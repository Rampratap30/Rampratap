import logging
import airflow
from airflow import AirflowException
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import boto3
from airflow.models import Variable
import json
from botocore.exceptions import ClientError
import pymysql
import pendulum
import csv
# from airflow.utils.email import send_email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from datetime import datetime as dt
import requests
import time
import calendar
from datetime import timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the local timezone to US/Eastern
local_tz = pendulum.timezone("US/Eastern")

DAG_NAME = 'RAC_TECH_MASTER_DAILY_NOTIFICATION'

current_datetime_utc = datetime.now(local_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
formatted_current_datetime_utc = datetime.now(
    local_tz).strftime('%Y-%m-%d %H:%M:%S')
current_date = datetime.now(local_tz).strftime('%Y-%m-%d')
# Set the start date to 11 PM EST
start_date = datetime(2023, 10, 25, 23, 0, 0, tzinfo=local_tz)

default_args = {
    'owner': 'Airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id=DAG_NAME,
    default_args=default_args,
    # This triggers the DAG daily at 11 PM US/Eastern time
    schedule_interval='0 23 * * *',
    catchup=False,
)

AWS_SECRETS_MYSQL = Variable.get('AWS_SECRETS_MYSQL')
SMTP_SERVER = Variable.get('SMTP_SERVER')
FROM_ADDRESS = Variable.get('FROM_ADDRESS')
AWS_SECRETS_S3 = Variable.get('AWS_SECRETS_S3')
TECH_MASTER_ENV = Variable.get('TECH_MASTER_ENV')

TECH_MASTER_S3_BUCKET = Variable.get('TECH_MASTER_S3_BUCKET')
S3_EXPORT_PENDING_APPROVAL_PATH = Variable.get(
    'S3_EXPORT_PENDING_APPROVAL_PATH')
S3_EXPORT_ALLChanges_PATH = Variable.get('S3_EXPORT_ALLChanges_PATH')

S3_EXPORT_PROCESSED_RECORDS = Variable.get('S3_EXPORT_PROCESSED_RECORDS')
TECH_MASTER_INCOMPLETE_RECORD_EXECUTION = Variable.get('TECH_MASTER_INCOMPLETE_RECORD_EXECUTION')


# Define functions for database connection and data retrieval


def get_secret_value(secretID):
    try:
        region = "us-east-1"
        serviceName = "secretsmanager"
        if secretID is None:
            raise Exception("Secret ID is missing.")
        secretsmanager_client = boto3.client(
            service_name=serviceName, region_name=region)
        kwargs = {"SecretId": secretID}
        response = secretsmanager_client.get_secret_value(**kwargs)
        return json.loads(response["SecretString"])
    except ClientError as error:
        raise Exception(f"Error in secret manager: {str(error)}")


secretDit = get_secret_value(AWS_SECRETS_MYSQL)
s3_secretDit = get_secret_value(AWS_SECRETS_S3)
s3KeyId = s3_secretDit["aws_access_key_id"]
s3AccessKey = s3_secretDit["aws_secret_access_key"]


class DatabaseConnection:
    def __init__(self):
        self.host = secretDit["host"]
        self.username = secretDit["username"]
        self.password = secretDit["password"]
        self.db_name = secretDit["dbname"]
        self.port = int(secretDit["port"])

    def connect(self):
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port,
                db=self.db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            logging.error(f"Error connecting to the database: {str(e)}")
            raise Exception(f"Error connecting to the database: {str(e)}")

def fetch_username_database(id):
    query = """
        SELECT RAC_FS_TM_GET_USER_NAME (%s) AS USER_NAME
    """

    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            username = cursor.fetchone()
            if username:
                return username
            else:
                return None
    except Exception as e:
        print(str(e), "Error fetching fetch_username_database")
        return None

def format_datetime(dt):
    if dt is not None and dt != '0000-00-00 00:00:00':
        if isinstance(dt, str):
            # Convert the string to a datetime object
            dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        return dt.strftime('%m-%d-%Y')
    return ''


def airflow_last_run_timestamp():

    _is_exists_query = "select * from RAC_FS_TM_REQ_CLMS where `FIELD_NAME` = 'AIRFLOW_DAILY_NOTIFICATION'"
    insert_query = """ 
        insert into RAC_FS_TM_REQ_CLMS 
        set 
        `FIELD_NAME` = 'AIRFLOW_DAILY_NOTIFICATION',
        `APPROVAL_REQ` = 'Y',
        `CREATION_DATE` = %s,
        `CREATED_BY` = 'AWS',
        `LAST_UPDATE_DATE` = %s,
        `LAST_UPDATED_BY` = 'AWS',
        `ATTRIBUTE1` = %s
    """

    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            # Check if the record exists
            cursor.execute(_is_exists_query)
            records = cursor.fetchone()
            if records:
                # Return the record as a dictionary
                record_dict = {
                    'FIELD_NAME': records['FIELD_NAME'],
                    'APPROVAL_REQ': records['APPROVAL_REQ'],
                    'CREATION_DATE': records['CREATION_DATE'],
                    'CREATED_BY': records['CREATED_BY'],
                    'LAST_UPDATE_DATE': records['LAST_UPDATE_DATE'],
                    'LAST_UPDATED_BY': records['LAST_UPDATED_BY'],
                    'ATTRIBUTE1': records['ATTRIBUTE1']
                }
                return record_dict
            else:
                cursor.execute(insert_query, (current_datetime_utc,
                               current_datetime_utc, formatted_current_datetime_utc))
                connection.commit()
                connection.close()
                return {'ATTRIBUTE1': formatted_current_datetime_utc}
    except Exception as e:
        print(str(e), "Error fetching/inserting records from the database")
        logger.error(
            'Error fetching/inserting records from the database: %s', str(e))


def airflow_processed_record_last_run_timestamp():

    _is_exists_query = "select * from RAC_FS_TM_REQ_CLMS where `FIELD_NAME` = 'AIRFLOW_PROCESSED_RECORD_DAILY_NOTIFICATION'"
    insert_query = """ 
        insert into RAC_FS_TM_REQ_CLMS 
        set 
        `FIELD_NAME` = 'AIRFLOW_PROCESSED_RECORD_DAILY_NOTIFICATION',
        `APPROVAL_REQ` = 'Y',
        `CREATION_DATE` = %s,
        `CREATED_BY` = 'AWS',
        `LAST_UPDATE_DATE` = %s,
        `LAST_UPDATED_BY` = 'AWS',
        `ATTRIBUTE1` = %s
    """

    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            # Check if the record exists
            cursor.execute(_is_exists_query)
            records = cursor.fetchone()
            if records:
                # Return the record as a dictionary
                record_dict = {
                    'FIELD_NAME': records['FIELD_NAME'],
                    'APPROVAL_REQ': records['APPROVAL_REQ'],
                    'CREATION_DATE': records['CREATION_DATE'],
                    'CREATED_BY': records['CREATED_BY'],
                    'LAST_UPDATE_DATE': records['LAST_UPDATE_DATE'],
                    'LAST_UPDATED_BY': records['LAST_UPDATED_BY'],
                    'ATTRIBUTE1': records['ATTRIBUTE1']
                }
                return record_dict
            else:
                cursor.execute(insert_query, (current_datetime_utc,
                               current_datetime_utc, formatted_current_datetime_utc))
                connection.commit()
                connection.close()
                return {'ATTRIBUTE1': formatted_current_datetime_utc}
    except Exception as e:
        print(str(e), "Error fetching/inserting records from the database")
        logger.error(
            'Error fetching/inserting records from the database: %s', str(e))


def update_last_run_timestamp(connection, current_datetime_utc, filed_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE RAC_FS_TM_REQ_CLMS SET ATTRIBUTE1 = %s WHERE FIELD_NAME = %s",
                           (current_datetime_utc, filed_name,))
            connection.commit()
        return True
    except Exception as e:
        logger.error(f"Error while updating: {str(e)}")
        return False


def create_daily_notif_csv_from_records(records):
    csv_file = '/tmp/daily_exported_data.csv'
    fieldnames = ['Change ID', 'Change Type', 'Requested By', 'Change Note', 'Change Effective Date', 'Region', 'Area Short', 'Location Code',
                  'Manager Employee ID', 'Employee ID', 'Resource Number', 'Employee Name', 'Employee Email',
                  'Job Title', 'Job Type', 'Job ADP Code', 'Team Type',
                  'Work Shift (1st, 2nd, 3rd)', 'On Call', 'On Site', 'Dedicated', 'Dedicated To',
                  'Service Advantage', 'FS Status', 'Service Start Date', 'Service End Date', 'Record Complete',
                  'Manager Flag', 'Admin Notes', 'Review Date', 'CSA Change Comment',
                  'CSA Notification Required', 'CSA Notification Complete', 'Creation Date']

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:

            emp_info = get_emp_info(record.get('EMPLOYEE_ID'))

            record_complete_value = record.get('RECORD_COMPLETE', '')
            if record_complete_value is not None:
                record_complete_value = record_complete_value.strip()
            else:
                record_complete_value = ''
            username = fetch_username_database(record.get('REQUESTED_BY'))
            writer.writerow({
                'Change ID': record.get('CHANGE_ID', ''),
                'Change Type': record.get('CHANGE_TYPE', ''),
                'Requested By': username["USER_NAME"] if username else record.get('REQUESTED_BY'),
                'Change Note': record.get('CHANGE_NOTE', ''),
                'Change Effective Date': format_datetime(record.get('CHANGE_EFFECTIVE_DATE')),
                'Region': record.get('REGION', ''),
                'Area Short': record.get('AREA', ''),
                'Location Code': record.get('LOC_CODE', ''),
                'Manager Employee ID': record.get('MANAGER_ID', ''),
                'Employee ID': record.get('EMPLOYEE_ID', ''),
                'Resource Number': emp_info['RESOURCE_NUMBER'] if emp_info else None,
                'Employee Name': emp_info['EMPLOYEE_NAME'] if emp_info else None,
                'Employee Email': emp_info['EMAIL'] if emp_info else None,
                'Job Title': record.get('JOB_TITLE', ''),
                'Job Type': record.get('JOB_TYPE', ''),
                'Job ADP Code': record.get('JOB_ADP', ''),
                'Team Type': record.get('TEAM_TYPE', ''),
                'Work Shift (1st, 2nd, 3rd)': record.get('WORK_SHIFT', ''),
                'On Call': record.get('ON_CALL', ''),
                'On Site': record.get('ON_SITE', ''),
                'Dedicated': record.get('DEDICATED', ''),
                'Dedicated To': record.get('DEDICATED_TO', ''),
                'Service Advantage': record.get('SERVICE_ADVANTAGE', ''),
                'FS Status': record.get('FS_STATUS', ''),
                'Service Start Date': format_datetime(record.get('SERVICE_START_DATE')),
                'Service End Date': format_datetime(record.get('SERVICE_END_DATE')),
                'Record Complete': record_complete_value,
                'Manager Flag': record.get('MANAGER_FLAG', ''),
                'Admin Notes': record.get('ADMIN_NOTES', ''),
                'Review Date': format_datetime(record.get('REVIEW_DATE')),
                'CSA Change Comment': record.get('CSA_CHANGE_COMMENT', ''),
                'CSA Notification Required': record.get('CSA_NOTIFICATION_REQUIRED', ''),
                'CSA Notification Complete': record.get('CSA_NOTIFICATION_COMPLETE', ''),
                'Creation Date': format_datetime(record.get('CREATION_DATE')),
            })

    return csv_file


def notification_records(type=None, **kwargs):

    query = """
        SELECT
            a.CHANGE_ID,
            a.CHANGE_NOTE,
            a.CHANGE_EFFECTIVE_DATE,
            a.REGION,
            a.AREA,
            a.LOC_CODE,
            a.EMPLOYEE_ID,
            (SELECT 
                    concat(c.EMPLOYEE_NAME,' | ', c.EMAIL,' | ', c.RESOURCE_NUMBER)
                FROM
                    RAC_FS_TM_EMPLOYEE_DTLS as b
                    inner join RAC_HR_TM_EMPLOYEE_DTLS as c on b.EMPLOYEE_ID = c.EMPLOYEE_ID
                WHERE
                    b.EMPLOYEE_ID = a.EMPLOYEE_ID) AS emp_info,
            a.JOB_TITLE,
            a.JOB_TYPE,
            a.JOB_ADP,
            a.TEAM_TYPE,
            a.WORK_SHIFT,
            a.ON_CALL,
            a.ON_SITE,
            a.DEDICATED,
            a.DEDICATED_TO,
            a.SERVICE_ADVANTAGE,
            a.FS_STATUS,
            a.SERVICE_START_DATE,
            a.SERVICE_END_DATE,
            a.RECORD_COMPLETE,
            a.MANAGER_FLAG,
            a.ADMIN_NOTES,
            a.REVIEW_DATE,
            a.MANAGER_ID,
            a.REQUESTED_BY,
            a.CHANGE_TYPE,
            a.CSA_CHANGE_COMMENT,
            a.CSA_NOTIFICATION_REQUIRED,
            a.CSA_NOTIFICATION_COMPLETE,
            a.CREATION_DATE
        FROM
            RAC_FS_TM_EMPLOYEE_UPD AS a
    """

    if type == "LAST_24_HOURS_RECORDS":
        airflow_info = airflow_last_run_timestamp()
        logger.info(f"airflow last run time info : {airflow_info}")
        if airflow_info:
            last_run_timestamp = airflow_info.get('ATTRIBUTE1')
        else:
            last_run_timestamp = formatted_current_datetime_utc
        logger.info(f"last_run_timestamp : {last_run_timestamp}")

        query += f" WHERE a.LAST_UPDATE_DATE between '{last_run_timestamp}' and UTC_TIMESTAMP()"
    elif type == "PENDING_RECORDS":
        query += " WHERE a.CHANGE_STATUS = 'Pending'"
    elif type == "APPROVED_RECORDS":
        query += " WHERE a.CHANGE_STATUS = 'Approved'"
    elif type == "PROCESSED_RECORDS":
        airflow_info = airflow_processed_record_last_run_timestamp()
        logger.info(
            f"airflow processed record last run time info : {airflow_info}")
        if airflow_info:
            last_run_timestamp = airflow_info.get('ATTRIBUTE1')
        else:
            last_run_timestamp = formatted_current_datetime_utc
        logger.info(f"last_run_timestamp : {last_run_timestamp}")

        query += f" WHERE a.LAST_UPDATE_DATE between '{last_run_timestamp}' and UTC_TIMESTAMP()"
        query += " and a.CHANGE_STATUS = 'Processed'"
        query += " and (a.ATTRIBUTE1 <> 'Manager_Transfer' or a.ATTRIBUTE1 is null)"
        query += " and a.REQUESTED_BY <> 'OFSC'"
        if 'manager_id' in kwargs and kwargs['manager_id'] is not None:
            query += f" AND a.MANAGER_ID = {kwargs['manager_id']}"
    else:
        return None

    logger.info(f"type = {type} query : {query}")
    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            connection.close()
        return records
    except Exception as e:
        print(str(e), "notification_records")
        logging.info(
            'Error notification_records from the database: %s', str(e))
        connection.close()
        return None


def get_manager_ids(connection):
    try:
        airflow_info = airflow_processed_record_last_run_timestamp()
        if airflow_info:
            last_run_timestamp = airflow_info.get('ATTRIBUTE1')
        else:
            last_run_timestamp = formatted_current_datetime_utc
        logger.info(
            f"get_manager_ids : last_run_timestamp : {last_run_timestamp}")
        with connection.cursor() as cursor:
            query = """
                    SELECT
                        a.MANAGER_ID
                    FROM RAC_FS_TM_EMPLOYEE_UPD AS a
                    INNER JOIN RAC_HR_TM_EMPLOYEE_DTLS as b ON a.EMPLOYEE_ID = b.EMPLOYEE_ID
                """
            query += f" WHERE a.LAST_UPDATE_DATE BETWEEN '{last_run_timestamp}' AND UTC_TIMESTAMP()"
            query += " AND a.CHANGE_STATUS = 'Processed'"
            query += " AND (a.ATTRIBUTE1 <> 'Manager_Transfer' OR a.ATTRIBUTE1 IS NULL)"
            query += " AND a.REQUESTED_BY <> 'OFSC'"
            query += " GROUP BY a.MANAGER_ID"
            cursor.execute(query)
            recipients = cursor.fetchall()
            return recipients
    except Exception as e:
        logging.error("Error fetching manager emails: %s", str(e))
        return []


def upload_csv_to_s3(csv_file, s3_bucket, s3_key):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(csv_file, s3_bucket, s3_key)
        logging.info(
            f"Uploaded {csv_file} to S3 bucket {s3_bucket} with key {s3_key}")
    except Exception as e:
        logging.error(f"Error uploading {csv_file} to S3: {str(e)}")


def generate_presigned_url(s3_bucket, s3_key):
    s3_client = boto3.client('s3', region_name='us-east-1',
                             aws_access_key_id=s3KeyId, aws_secret_access_key=s3AccessKey)
    url = s3_client.generate_presigned_url(
        'get_object', Params={'Bucket': s3_bucket, 'Key': s3_key}, ExpiresIn=432000)
    return url


def send_email(recipient_email, subject, body):
    try:
        smtp_server = SMTP_SERVER
        from_address = FROM_ADDRESS

        if not smtp_server or not from_address:
            raise ValueError("SMTP_SERVER or FROM_ADDRESS are not set.")

        msg = EmailMessage()
        msg.set_content(body)
        msg.add_alternative(body, subtype='html')
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = recipient_email

        logger.info(recipient_email, "recipient_email")
        smtp_client = smtplib.SMTP(smtp_server)
        smtp_client.sendmail(from_address, recipient_email, msg.as_string())
        smtp_client.quit()

        logger.info("Email sent successfully")

        return "Email Sent"

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return "Email Error"


def get_csa_change_id_records():

    query = "select * from RAC_FS_TM_EMPLOYEE_UPD where DATE_FORMAT(CHANGE_EFFECTIVE_DATE,'%Y-%m-%d') <= utc_timestamp() and CHANGE_STATUS = 'Approved'"

    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                return records
            else:
                return None
    except Exception as e:
        print(str(e), "Error fetching get_csa_change_id_records from the database")
        logger.error(
            'Error fetchingget_csa_change_id_records from the database: %s', str(e))


def get_manager_transfer_records():

    query = "select * from RAC_FS_TM_EMPLOYEE_UPD where ATTRIBUTE1 = 'Manager_Transfer'  and ATTRIBUTE2 is not null and ATTRIBUTE3 is null and CHANGE_STATUS = 'Processed'"

    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                return records
            else:
                return None
    except Exception as e:
        print(str(e), "Error fetching get_manager_transfer_records from the database")
        logger.error(
            'Error get_manager_transfer_records from the database: %s', str(e))


def get_incompleted_records():

    query = "select * from RAC_FS_TM_EMPLOYEE_DTLS where RECORD_COMPLETE != 'Y' group by MANAGER_ID"
    
    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                return records
            else:
                return None
    except Exception as e:
        print(str(e), "Error fetching get_incompleted_records from the database")
        logger.error(
            'Error get_incompleted_records from the database: %s', str(e))


def get_area_dir_info(employee_id):
    query = """
        SELECT
            e.EMPLOYEE_ID,
            e.EMPLOYEE_NAME,
            e.RESOURCE_NUMBER,
            e.EMAIL
        FROM RAC_FS_TM_EMPLOYEE_DTLS a
        LEFT OUTER JOIN RAC_FS_TM_AREA c ON a.AREA_ID = c.AREA_ID
        LEFT OUTER JOIN RAC_HR_TM_EMPLOYEE_DTLS e ON c.AREA_DIR_EMP_ID = e.EMPLOYEE_ID
        WHERE a.EMPLOYEE_ID = %s 
    """

    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))
            records = cursor.fetchone()
            if records:
                return records
            else:
                return None
    except Exception as e:
        print(str(e), "Error fetching get_area_dir_info from the database")
        logger.error('Error get_area_dir_info from the database: %s', str(e))


def get_emp_info(employee_id):
    query = """
        SELECT
            EMPLOYEE_NAME,
            RESOURCE_NUMBER,
            EMAIL
        FROM RAC_HR_TM_EMPLOYEE_DTLS
        WHERE EMPLOYEE_ID = %s 
    """

    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))
            records = cursor.fetchone()
            if records:
                return records
            else:
                return None
    except Exception as e:
        print(str(e), "Error fetching get_emp_info from the database")
        logger.error('Error get_emp_info from the database: %s', str(e))


def DAILY_LAST_24_HRS_RECORDS_NOTIFICATION(**kwargs):
    try:
        connection = DatabaseConnection().connect()
        records = notification_records(type="LAST_24_HOURS_RECORDS")
        logger.info(f"TECH_MASTER_ENV: {TECH_MASTER_ENV}")
        logger.info(f"current_datetime_utc : {current_datetime_utc}")
        logger.info(
            f"formatted_current_datetime_utc: {formatted_current_datetime_utc}")

        if records:
            csv_file_path = create_daily_notif_csv_from_records(records)
            s3_bucket = TECH_MASTER_S3_BUCKET
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            logger.info(f"timestamp : {timestamp}")
            file_name_format = f"{timestamp}_daily_changes_notification_techmaster_v1.csv"
            s3_key = f"{TECH_MASTER_ENV}/{S3_EXPORT_ALLChanges_PATH}/{file_name_format}"

            upload_csv_to_s3(csv_file_path, s3_bucket, s3_key)
            presigned_url = generate_presigned_url(s3_bucket, s3_key)
            logger.info(f"presigned_url : {presigned_url}")

            # Send emails to the recipients
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM RAC_FS_TM_NOTIF WHERE STATUS = 'ACTIVE' and NOTIFICATION_NAME = 'Daily Changes'")
                recipients = cursor.fetchall()
                for recipient in recipients:
                    recipient_email = recipient["EMAIL_ID"]
                    airflow_info = airflow_last_run_timestamp()
                    logger.info(f"airflow last run time info : {airflow_info}")
                    if airflow_info:
                        last_run_timestamp = airflow_info.get('ATTRIBUTE1')
                    subject = f"Techmaster Changes All for {last_run_timestamp} - {formatted_current_datetime_utc}"
                    body = f"Dear All,<br><br>Please download Bulk export sheet using below link and it's valid for 5 days.<br><br><table><tr>"
                    body += f"<tr><td><a href={presigned_url}>Download</a></td></tr>"
                    body += f"<tr></table><br>NOTE: This is a system-generated email, ***No reply required***<br><br>Thank you"
                    email_status = send_email(recipient_email, subject, body)
                    if "Email Error" in email_status:
                        logger.info("Email status %s", email_status)
                    else:
                        logger.info("Email sent successfully to %s",
                                    recipient_email)

            # Update the timestamp
            update_last_run_timestamp(
                connection, formatted_current_datetime_utc, "AIRFLOW_DAILY_NOTIFICATION")
        else:
            logging.warning("No records found")

    except Exception as e:
        logging.error("Error in Daily Notification: %s", str(e))
    finally:
        if connection:
            connection.close()


def DAILY_NOTIFICATION_PENDING_RECORDS(**kwargs):
    try:
        connection = DatabaseConnection().connect()
        records = notification_records(type="PENDING_RECORDS")

        if records:
            csv_file_path = create_daily_notif_csv_from_records(records)
            s3_bucket = TECH_MASTER_S3_BUCKET
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            logger.info(f"timestamp : {timestamp}")
            file_name_format = f"{timestamp}_pending_techmaster_data_v1.csv"
            s3_key = f"{TECH_MASTER_ENV}/{S3_EXPORT_PENDING_APPROVAL_PATH}/{file_name_format}"

            upload_csv_to_s3(csv_file_path, s3_bucket, s3_key)
            presigned_url = generate_presigned_url(s3_bucket, s3_key)
            logger.info(f"presigned_url : {presigned_url}")

            # Send emails to the recipients
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM RAC_FS_TM_NOTIF WHERE STATUS = 'ACTIVE' and NOTIFICATION_NAME = 'Pending Approvals'")
                recipients = cursor.fetchall()
                for recipient in recipients:
                    recipient_email = recipient["EMAIL_ID"]
                    subject = "Techmaster Changes Pending Approval"
                    body = f"Dear All,<br><br>Please download Bulk export sheet using below link and it's valid for 5 days.<br><br><table><tr>"
                    body += f"<tr><td><a href={presigned_url}>Download</a></td></tr>"
                    body += f"<tr></table><br>NOTE: This is a system-generated email, ***No reply required***<br><br>Thank you"
                    email_status = send_email(recipient_email, subject, body)
                    if "Email Error" in email_status:
                        logger.info("Email status %s", email_status)
                    else:
                        logger.info("Email sent successfully to %s",
                                    recipient_email)
        else:
            logging.warning("No records found in pending notification.")

    except Exception as e:
        logging.error("Error in Pending Records Notification: %s", str(e))
    finally:
        if connection:
            connection.close()


def DAILY_PROCESSED_RECORDS_NOTIFICATION_TO_MANAGER(**kwargs):
    try:
        connection = DatabaseConnection().connect()
        _manager_info = get_manager_ids(connection)
        if _manager_info:
            for item in _manager_info:
                MANAGER_ID = item["MANAGER_ID"]
                records = notification_records(
                    type="PROCESSED_RECORDS", manager_id=MANAGER_ID)
                logger.info(f"TECH_MASTER_ENV: {TECH_MASTER_ENV}")
                logger.info(f"current_datetime_utc : {current_datetime_utc}")
                logger.info(
                    f"formatted_current_datetime_utc: {formatted_current_datetime_utc}")

                if records:
                    csv_file_path = create_daily_notif_csv_from_records(
                        records)
                    s3_bucket = TECH_MASTER_S3_BUCKET
                    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                    logger.info(f"timestamp : {timestamp}")
                    file_name_format = f"{timestamp}_{MANAGER_ID}_daily_processed_record_notification_techmaster_v1.csv"
                    s3_key = f"{TECH_MASTER_ENV}/{S3_EXPORT_PROCESSED_RECORDS}/{file_name_format}"

                    upload_csv_to_s3(csv_file_path, s3_bucket, s3_key)
                    presigned_url = generate_presigned_url(s3_bucket, s3_key)
                    logger.info(f"presigned_url : {presigned_url}")
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT EMAIL, EMPLOYEE_NAME as MANAGER_NAME FROM RAC_HR_TM_EMPLOYEE_DTLS where EMPLOYEE_ID = %s", (item['MANAGER_ID'],))
                        recipients = cursor.fetchone()
                        if recipients:
                            recipient_email = recipients["EMAIL"]
                            MANAGER_NAME = recipients['MANAGER_NAME']
                            subject = f"Techmaster Changes for {MANAGER_NAME} {current_date}"
                            body = f"Dear All,<br><br>Please download export sheet using below link and it's valid for 5 days.<br><br><table><tr>"
                            body += f"<tr><td><a href={presigned_url}>Download</a></td></tr>"
                            body += f"<tr></table><br>NOTE: This is a system-generated email, ***No reply required***<br><br>Thank you"
                            email_status = send_email(
                                recipient_email, subject, body)
                            if "Email Error" in email_status:
                                logger.info("Email status %s", email_status)
                            else:
                                logger.info(
                                    "Email sent successfully to %s", recipient_email)
            # Update the timestamp
            update_last_run_timestamp(
                connection, formatted_current_datetime_utc, "AIRFLOW_PROCESSED_RECORD_DAILY_NOTIFICATION")
        else:
            logging.warning("No records found")

    except Exception as e:
        logging.error("Error in Daily Notification: %s", str(e))
    finally:
        if connection:
            connection.close()


def INCOMPLETED_RECORD_NOTIFICATION(**kwargs):
    connection = None
    try:
        if TECH_MASTER_INCOMPLETE_RECORD_EXECUTION == "N":
            logging.info("Skipping job because it's not set to 'TECH_MASTER_INCOMPLETE_RECORD_EXECUTION = Y'.")
            return True
        
        connection = DatabaseConnection().connect()
        records = get_incompleted_records()

        if records:
            # Send emails to the recipients
            with connection.cursor() as cursor:
                for item in records:
                    cursor.execute(
                        "select * from RAC_FS_TM_EMPLOYEE_DTLS where MANAGER_ID = %s and RECORD_COMPLETE != 'Y'", (item['MANAGER_ID'],))
                    empInfo = cursor.fetchall()

                    # recipient email
                    cursor.execute(
                        "select * from RAC_HR_TM_EMPLOYEE_DTLS where EMPLOYEE_ID = %s", (item['MANAGER_ID'],))
                    recipients = cursor.fetchone()
                    recipient_email = recipients["EMAIL"]

                    subject = f"Techmaster Records Not Complete for Manager {recipients['EMPLOYEE_NAME']} {current_date}"
                    body = f"Dear {recipients['EMPLOYEE_NAME']}, <table><tr>"

                    body += f"</table><br><br>Matching Employee Details:<br><ul>"

                    for info in empInfo:
                        cursor.execute(
                            "select * from RAC_HR_TM_EMPLOYEE_DTLS where EMPLOYEE_ID = %s", (info['EMPLOYEE_ID'],))
                        _info = cursor.fetchone()
                        # Append the matching employee details to the email body
                        employee_name = _info['EMPLOYEE_NAME']
                        resource_number = _info['RESOURCE_NUMBER']
                        employee_id = _info['EMPLOYEE_ID']
                        body += f"<li>EID: {employee_id}, Resource Number: {resource_number}, Employee Name: {employee_name}</li>"

                    body += f"</ul><br>NOTE: This is a system-generated email, ***No reply required***<br><br>Thank you"
                    logger.info(f"body : {body}")
                    email_status = send_email(recipient_email, subject, body)
                    if "Email Error" in email_status:
                        logger.info("Email status %s", email_status)
                    else:
                        logger.info("Email sent successfully to %s",
                                    recipient_email)

        else:
            logging.warning("No records found")

    except Exception as e:
        logging.error("Error in incomplete record Notification: %s", str(e))
    finally:
        if connection:
            connection.close()

def format_value(value):
    return str(value) if value is not None else str("None")


def send_email_csa(recipient_email, old_data, new_data, subject=None):
    try:
        print("in email")
        smtp_server = SMTP_SERVER
        from_address = FROM_ADDRESS

        if not smtp_server or not from_address:
            raise ValueError("SMTP_SERVER or FROM_ADDRESS are not set.")

        # adding 6 sec delay
        time.sleep(6)

        print("Subject", subject)
        body = """<!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            table td, table tr {
                                border: 1px solid #AAAAAA;
                                padding: 7px;
                            }
                            table {
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                            }
                        </style>
                    </head>
                    <body>"""

        body += f"<br>The following changes have been applied to the Tech Master Database<br>"
        body += f"<table cellpadding='0' cellspacing='0' border='0' style='border-collapse: collapse;'>"
        body += f"<tbody>"
        body += "<tr><td>CSA Change Comment Log</td><td></td><td>" + format_value(new_data['CSA_CHANGE_COMMENT']) + "</td></tr>"
        body += "<tr><td>Last Edited Date</td><td></td><td>" + format_value(new_data['LAST_UPDATE_DATE']) + "</td></tr>"
        body += "<tr><td>Last Edited By</td><td></td><td>" + format_value(new_data['LAST_UPDATED_BY']) + "</td></tr>"
        body += "<tr><td>Creation Date</td><td>" + format_value(old_data['CREATION_DATE']) + "</td><td>" + format_value(new_data['CREATION_DATE']) + "</td></tr>"
        body += "<tr><td>Change Type</td><td></td><td>" + format_value(new_data['CHANGE_TYPE']) + "</td></tr>"
        body += "<tr><td>Employee ID</td><td>" + format_value(old_data['EMPLOYEE_ID']) + "</td><td>" + format_value(new_data['EMPLOYEE_ID']) + "</td></tr>"
        body += "<tr><td>Resource Number</td><td>" + format_value(old_data['RESOURCE_NUMBER']) + "</td><td>" + format_value(new_data['RESOURCE_NUMBER']) + "</td></tr>"
        body += "<tr><td>Employee Name</td><td>" + format_value(old_data['EMPLOYEE_NAME']) + "</td><td>" + format_value(new_data['EMPLOYEE_NAME']) + "</td></tr>"
        body += "<tr><td>Email Address</td><td>" + format_value(old_data['EMAIL']) + "</td><td>" + format_value(new_data['EMAIL']) + "</td></tr>"
        body += "<tr><td>FS Status</td><td>" + format_value(old_data['FS_STATUS']) + "</td><td>" + format_value(new_data['FS_STATUS']) + "</td></tr>"
        body += "<tr><td>Absence Start Date</td><td>" + (format_value(old_data['ABSENCE_START_DATE']) if old_data.get('ABSENCE_START_DATE') is not None else "None") + "</td><td>" + (format_value(new_data['ABSENCE_START_DATE']) if new_data.get('ABSENCE_START_DATE') is not None else "None") + "</td></tr>"
        body += "<tr><td>Absence End Date</td><td>" + (format_value(old_data['ABSENCE_END_DATE']) if old_data.get('ABSENCE_END_DATE') is not None else "None") + "</td><td>" + (format_value(new_data['ABSENCE_END_DATE']) if new_data.get('ABSENCE_END_DATE') is not None else "None") + "</td></tr>"
        body += "<tr><td>Region</td><td>" + format_value(old_data['REGION']) + "</td><td>" + format_value(new_data['REGION']) + "</td></tr>"
        body += "<tr><td>Area</td><td>" + format_value(old_data['AREA']) + "</td><td>" + format_value(new_data['AREA']) + "</td></tr>"
        body += "<tr><td>Location Code</td><td>" + format_value(old_data['LOC_CODE']) + "</td><td>" + format_value(new_data['LOC_CODE']) + "</td></tr>"
        body += "<tr><td>Manager Resource Number</td><td>" + format_value(old_data['MANAGER_RESOURCE_NUMBER']) + "</td><td>" + format_value(new_data['MANAGER_RESOURCE_NUMBER']) + "</td></tr>"
        body += "<tr><td>Manager Name</td><td>" + format_value(old_data['MANAGER_NAME']) + "</td><td>" + format_value(new_data['MANAGER_NAME']) + "</td></tr>"
        body += "<tr><td>Manager Email</td><td>" + format_value(old_data['MANAGER_EMAIL']) + "</td><td>" + format_value(new_data['MANAGER_EMAIL']) + "</td></tr>"
        body += "<tr><td>Area Dir Name</td><td>" + format_value(old_data['AREA_DIR_NAME']) + "</td><td>" + format_value(new_data['AREA_DIR_NAME']) + "</td></tr>"
        body += "<tr><td>Area Dir Email</td><td>" + format_value(old_data['AREA_DIR_EMAIL']) + "</td><td>" + format_value(new_data['AREA_DIR_EMAIL']) + "</td></tr>"
        body += "<tr><td>Team Type</td><td>" + format_value(old_data['TEAM_TYPE']) + "</td><td>" + format_value(new_data['TEAM_TYPE']) + "</td></tr>"
        body += "<tr><td>Additional Email</td><td>" + format_value(old_data['ALTERNATE_EMAIL']) + "</td><td>" + format_value(new_data['ALTERNATE_EMAIL']) + "</td></tr>"
        body += "<tr><td>Job Title</td><td>" + format_value(old_data['JOB_TITLE']) + "</td><td>" + format_value(new_data['JOB_TITLE']) + "</td></tr>"
        body += "<tr><td>Actual Termination Date</td><td>" + format_value(old_data['ACTUAL_TERMINATION_DATE']) + "</td><td>" + format_value(new_data['ACTUAL_TERMINATION_DATE']) + "</td></tr>"
        body += "<tr><td>Approved By</td><td>" + (format_value(old_data['APPROVED_BY']) if old_data.get('APPROVED_BY') is not None else "None") + "</td><td>" + (format_value(new_data['APPROVED_BY']) if new_data.get('APPROVED_BY') is not None else "None") + "</td></tr>"
        body += "<tr><td>Change Note</td><td>" + format_value(old_data['CHANGE_NOTE']) + "</td><td>" + format_value(new_data['CHANGE_NOTE']) + "</td></tr>"
        body += "<tr><td>HR Status</td><td>" + format_value(old_data['HR_STATUS']) + "</td><td>" + format_value(new_data['HR_STATUS']) + "</td></tr>"
        body += "<tr><td>Requested By</td><td>" + format_value(old_data['REQUESTED_BY']) + "</td><td>" + format_value(new_data['REQUESTED_BY'].strip()) + "</td></tr>"
        body += f"</tbody>"
        body += f"</table>"
        body += f"<br>NOTE : This is a system generated email,***No reply required***<br><br>Thank you"
        body += "</body></html>"

        msg = EmailMessage()
        msg.set_content(body)
        msg.add_alternative(body, subtype="html")
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = recipient_email
        smtp_client = smtplib.SMTP(smtp_server)
        smtp_client.sendmail(from_address, recipient_email, msg.as_string())
        smtp_client.quit()

        return "Email Sent"

    except Exception as e:
        print(e)
        return "Email Error"


def fetch_hierarchy_details(session, employee_id):
    try:
        # SQL query
        sql_query = """
            SELECT
              (SELECT CONCAT(EMPLOYEE_ID, ' | ', EMPLOYEE_NAME, ' | ', RESOURCE_NUMBER, ' | ', EMAIL)
               FROM RAC_HR_TM_EMPLOYEE_DTLS
               WHERE EMPLOYEE_ID = d.REGION_DIR_EMP_ID) AS region_dir_info,
              (SELECT CONCAT(EMPLOYEE_ID, ' | ', EMPLOYEE_NAME, ' | ', RESOURCE_NUMBER, ' | ', EMAIL)
               FROM RAC_HR_TM_EMPLOYEE_DTLS
               WHERE EMPLOYEE_ID = c.AREA_DIR_EMP_ID) AS area_dir_info,
              (SELECT CONCAT(EMPLOYEE_ID, ' | ', EMPLOYEE_NAME, ' | ', RESOURCE_NUMBER, ' | ', EMAIL)
               FROM RAC_HR_TM_EMPLOYEE_DTLS
               WHERE EMPLOYEE_ID = c.AREA_FOM_EMP_ID) AS area_fom_info,
              d.REGION_DIR_EMP_ID,
              c.AREA_DIR_EMP_ID,
              c.AREA_FOM_EMP_ID
            FROM RAC_FS_TM_EMPLOYEE_DTLS a
            LEFT OUTER JOIN RAC_FS_TM_AREA c ON a.AREA_ID = c.AREA_ID
            LEFT OUTER JOIN RAC_FS_TM_REGION d ON c.REGION_ID = d.REGION_ID
            WHERE a.EMPLOYEE_ID = :employee_id
        """

        # Execute SQL query and fetch the result
        result = session.execute(
            sql_query, {"employee_id": employee_id}).fetchone()

        hierarchy_details_section = {}
        if result:
            region_dir_info = (
                result[0].split(" | ") if result[0] else [
                    None, None, None, None]
            )
            hierarchy_details_section["region_dir_employee_id"] = (
                region_dir_info[0].strip() if region_dir_info[0] else None
            )
            hierarchy_details_section["region_dir_employee_name"] = (
                region_dir_info[1].strip() if region_dir_info[1] else None
            )
            hierarchy_details_section["region_dir_resource_number"] = (
                region_dir_info[2].strip() if region_dir_info[2] else None
            )
            hierarchy_details_section["region_dir_email"] = (
                region_dir_info[3].strip() if region_dir_info[3] else None
            )

            area_dir_info = (
                result[1].split(" | ") if result[1] else [
                    None, None, None, None]
            )
            hierarchy_details_section["area_dir_employee_id"] = (
                area_dir_info[0].strip() if area_dir_info[0] else None
            )
            hierarchy_details_section["area_dir_employee_name"] = (
                area_dir_info[1].strip() if area_dir_info[1] else None
            )
            hierarchy_details_section["area_dir_resource_number"] = (
                area_dir_info[2].strip() if area_dir_info[2] else None
            )
            hierarchy_details_section["area_dir_email"] = (
                area_dir_info[3].strip() if area_dir_info[3] else None
            )

            area_fom_info = (
                result[2].split(" | ") if result[2] else [
                    None, None, None, None]
            )
            hierarchy_details_section["area_fom_employee_id"] = (
                area_fom_info[0].strip() if area_fom_info[0] else None
            )
            hierarchy_details_section["area_fom_employee_name"] = (
                area_fom_info[1].strip() if area_fom_info[1] else None
            )
            hierarchy_details_section["area_fom_resource_number"] = (
                area_fom_info[2].strip() if area_fom_info[2] else None
            )
            hierarchy_details_section["area_fom_email"] = (
                area_fom_info[3].strip() if area_fom_info[3] else None
            )

            return hierarchy_details_section

        # Populate hierarchy_details_section if no result
        return {
            "region_dir_employee_id": None,
            "region_dir_employee_name": None,
            "region_dir_resource_number": None,
            "region_dir_email": None,
            "area_dir_employee_id": None,
            "area_dir_employee_name": None,
            "area_dir_resource_number": None,
            "area_dir_email": None,
            "area_fom_employee_id": None,
            "area_fom_employee_name": None,
            "area_fom_resource_number": None,
            "area_fom_email": None,
        }

    except Exception as e:
        # Handle any exceptions and return default values
        return {
            "region_dir_employee_id": None,
            "region_dir_employee_name": None,
            "region_dir_resource_number": None,
            "region_dir_email": None,
            "area_dir_employee_id": None,
            "area_dir_employee_name": None,
            "area_dir_resource_number": None,
            "area_dir_email": None,
            "area_fom_employee_id": None,
            "area_fom_employee_name": None,
            "area_fom_resource_number": None,
            "area_fom_email": None,
        }


def CSA_NOTIFICATION_APPROVED_RECORDS(**kwargs):
    try:
        connection = DatabaseConnection().connect()
        records = get_csa_change_id_records()

        if records:
            with connection.cursor() as cursor:
                for item in records:
                    try:
                        cursor.execute(
                            "SELECT * FROM RAC_FS_TM_EMPLOYEE_DTLS WHERE EMPLOYEE_ID = %s", (item['EMPLOYEE_ID'],))
                        emp_update_query = cursor.fetchone()

                        sql_get_name = """ SELECT RAC_FS_TM_GET_USER_NAME (%s) AS USER_NAME """

                        if item["AREA"] is not None:
                            area_concatenated = "%" + \
                                item["AREA"] + "%"
                        else:
                            area_concatenated = ""

                        if item["JOB_ADP"] is not None:
                            job_adp_concatenated = "%" + \
                                item["JOB_ADP"] + "%"
                        else:
                            job_adp_concatenated = ""

                        if item["TEAM_TYPE"] is not None:
                            team_type_concatenated = "%" + \
                                item["TEAM_TYPE"] + "%"
                        else:
                            team_type_concatenated = ""

                        cursor.execute(
                            "SELECT AREA_ID, AREA_SHORT_NAME FROM RAC_FS_TM_AREA WHERE AREA_SHORT_NAME LIKE %s", (area_concatenated,))
                        area_result = cursor.fetchone()

                        cursor.execute(
                            "SELECT JOB_ID, JOB_TITLE FROM RAC_FS_TM_JOB_CODE WHERE JOB_ADP_CODE LIKE %s", (job_adp_concatenated))
                        job_result = cursor.fetchone()

                        cursor.execute(
                            "SELECT TEAM_TYPE_ID, TEAM_TYPE_NAME FROM RAC_FS_TM_TEAM_TYPE WHERE TEAM_TYPE_NAME LIKE %s", (team_type_concatenated,))
                        team_result = cursor.fetchone()

                        if area_result:
                            area_id = area_result["AREA_ID"]
                        else:
                            area_id = None

                        if job_result:
                            job_id = job_result["JOB_ID"]
                        else:
                            job_id = None

                        if team_result:
                            team_type_id = team_result["TEAM_TYPE_ID"]
                        else:
                            team_type_id = None

                        # If employee not present in TM, need to insert in TM table.

                        if emp_update_query is None:
                            insert_stmt = """
                                INSERT INTO RAC_FS_TM_EMPLOYEE_DTLS
                                SET
                                    EMPLOYEE_ID = %s,
                                    EMPLOYEE_NAME = %s,
                                    AREA_ID = %s,
                                    LOCATION_CODE = %s,
                                    MANAGER_ID = %s,
                                    MANAGER_FLAG = %s,
                                    JOB_ID = %s,
                                    TEAM_TYPE_ID = %s,
                                    WORK_SHIFT = %s,
                                    ON_CALL = %s,
                                    ON_SITE = %s,
                                    DEDICATED = %s,
                                    DEDICATED_TO = %s,
                                    BUSINESS_ORG = %s,
                                    SERVICE_ADVANTAGE = %s,
                                    SERVICE_START_DATE = %s,
                                    SERVICE_END_DATE = %s,
                                    FS_STATUS = %s,
                                    RECORD_COMPLETE = %s,
                                    ADMIN_NOTES = %s,
                                    LAST_UPDATE_DATE = %s,
                                    LAST_UPDATED_BY = %s,
                                    ABSENCE_START_DATE = %s,
                                    ABSENCE_END_DATE = %s,
                                    ACTUAL_RETURN_TO_WORK = %s,
                                    ALTERNATE_EMAIL = %s,
                                    PRODUCTION_PRINT = %s,
                                    OFSC_STATUS = %s,
                                    HR_STATUS = %s,
                                    REVIEW_DATE = %s
                            """
                            cursor.execute(
                                insert_stmt,
                                (
                                    item['EMPLOYEE_ID'],
                                    item["EMPLOYEE_NAME"],
                                    area_id,
                                    item['LOC_CODE'],
                                    item["MANAGER_ID"],
                                    item["MANAGER_FLAG"],
                                    job_id,
                                    team_type_id,
                                    item["WORK_SHIFT"],
                                    item['ON_CALL'],
                                    item["ON_SITE"],
                                    item["DEDICATED"],
                                    item['DEDICATED_TO'],
                                    item["BUSINESS_ORG"],
                                    item["SERVICE_ADVANTAGE"],
                                    item['SERVICE_START_DATE'],
                                    item["SERVICE_END_DATE"],
                                    item["FS_STATUS"],
                                    item['RECORD_COMPLETE'],
                                    item["ADMIN_NOTES"],
                                    current_datetime_utc,
                                    item["LAST_UPDATED_BY"],
                                    item["ABSENCE_START_DATE"],
                                    item["ABSENCE_END_DATE"],
                                    item["ACTUAL_RETURN_TO_WORK"],
                                    item["ALTERNATE_EMAIL"],
                                    item["PRODUCTION_PRINT"],
                                    item["OFSC_STATUS"],
                                    item["HR_STATUS"],
                                    item["REVIEW_DATE"],
                                )
                            )

                        # Commit the changes to the database
                        connection.commit()

                        cursor.execute(
                            "SELECT * FROM RAC_FS_TM_EMPLOYEE_DTLS WHERE EMPLOYEE_ID = %s", (item['EMPLOYEE_ID'],))
                        emp_update_query = cursor.fetchone()

                        if emp_update_query:
                            employee_id = emp_update_query['EMPLOYEE_ID']

                            # Convert integer values to strings before concatenation
                            if item["MANAGER_ID"] is not None:
                                manager_id_str = str(item["MANAGER_ID"])
                            else:
                                manager_id_str = ""

                            # get hierarchy info
                            hierarchy = get_area_dir_info(employee_id)

                            sql_query = """
                                SELECT EMP.RESOURCE_NUMBER, FS_EMP.EMPLOYEE_NAME, REGION.REGION_NAME,
                                AREA.AREA_SHORT_NAME, TEAM.TEAM_TYPE_NAME,
                                JOB.JOB_TITLE, EMP.ACTUAL_TERMINATION_DATE, FS_EMP.HR_STATUS,
                                FS_EMP.ALTERNATE_EMAIL, EMP.EMAIL, FS_EMP.SERVICE_END_DATE
                                FROM RAC_FS_TM_EMPLOYEE_DTLS FS_EMP
                                JOIN RAC_HR_TM_EMPLOYEE_DTLS EMP ON EMP.EMPLOYEE_ID = FS_EMP.EMPLOYEE_ID
                                LEFT JOIN RAC_FS_TM_AREA AREA ON AREA.AREA_ID = FS_EMP.AREA_ID
                                LEFT JOIN RAC_FS_TM_REGION REGION ON REGION.REGION_ID = AREA.REGION_ID
                                LEFT JOIN RAC_FS_TM_TEAM_TYPE TEAM ON TEAM.TEAM_TYPE_ID = FS_EMP.TEAM_TYPE_ID
                                LEFT JOIN RAC_FS_TM_JOB_CODE JOB ON JOB.JOB_ID = FS_EMP.JOB_ID
                                WHERE FS_EMP.EMPLOYEE_ID = %s
                            """
                            cursor.execute(sql_query, (employee_id,))
                            old_result = cursor.fetchone()
                            if old_result:
                                sql_query = """
                                        select b.EMAIL AS MANAGER_EMAIL, b.EMPLOYEE_NAME AS MANAGER_NAME, b.RESOURCE_NUMBER AS MANAGER_RESOURCE_NUMBER 
                                        from RAC_FS_TM_EMPLOYEE_DTLS as a inner join
                                        RAC_HR_TM_EMPLOYEE_DTLS as b on a.MANAGER_ID = b.EMPLOYEE_ID 
                                        where a.EMPLOYEE_ID  = %s
                                    """
                                cursor.execute(sql_query, (employee_id,))
                                manager_Info = cursor.fetchone()
                                cursor.execute(
                                    sql_get_name, (
                                        emp_update_query["LAST_UPDATED_BY"],)
                                )
                                last_updated_name = cursor.fetchone()
                                alternate_email = None
                                if item["ALTERNATE_EMAIL_OLD"]:
                                    alternate_email = item["ALTERNATE_EMAIL_OLD"]
                                else:
                                    alternate_email = old_result["ALTERNATE_EMAIL"]
                                old_data = {
                                    "CSA_CHANGE_COMMENT": None,
                                    "LAST_UPDATE_DATE": emp_update_query["LAST_UPDATE_DATE"],
                                    "LAST_UPDATED_BY": last_updated_name["USER_NAME"],
                                    "CREATION_DATE": emp_update_query["CREATION_DATE"],
                                    "CHANGE_TYPE": None,
                                    "EMPLOYEE_ID": emp_update_query["EMPLOYEE_ID"],
                                    "RESOURCE_NUMBER": old_result["RESOURCE_NUMBER"],
                                    "EMPLOYEE_NAME": old_result["EMPLOYEE_NAME"],
                                    "EMAIL": old_result["EMAIL"],
                                    "FS_STATUS": emp_update_query["FS_STATUS"],
                                    "REGION": old_result["REGION_NAME"],
                                    "AREA": old_result["AREA_SHORT_NAME"],
                                    "LOC_CODE": emp_update_query["LOCATION_CODE"],
                                    "MANAGER_RESOURCE_NUMBER": manager_Info["MANAGER_RESOURCE_NUMBER"] if manager_Info else None,
                                    "MANAGER_NAME": manager_Info["MANAGER_NAME"] if manager_Info else None,
                                    "MANAGER_EMAIL": manager_Info["MANAGER_EMAIL"] if manager_Info else None,
                                    "AREA_DIR_NAME": hierarchy["EMPLOYEE_NAME"] if hierarchy else None,
                                    "AREA_DIR_EMAIL": hierarchy["EMAIL"] if hierarchy else None,
                                    "TEAM_TYPE": old_result["TEAM_TYPE_NAME"],
                                    "ALTERNATE_EMAIL": alternate_email,
                                    "JOB_TITLE": old_result["JOB_TITLE"],
                                    "ACTUAL_TERMINATION_DATE": None,
                                    "APPROVED_BY": None,
                                    "CHANGE_NOTE": None,
                                    "HR_STATUS": old_result["HR_STATUS"],
                                    "REQUESTED_BY": None,
                                    "ABSENCE_START_DATE": emp_update_query["ABSENCE_START_DATE"],
                                    "ABSENCE_END_DATE": emp_update_query["ABSENCE_END_DATE"],
                                }

                                if item["ATTRIBUTE1"] == "manager":
                                    _emp_update_query = """
                                        UPDATE RAC_FS_TM_EMPLOYEE_DTLS
                                        SET
                                            MANAGER_ID = %s,
                                            LAST_UPDATE_DATE = %s,
                                            LAST_UPDATED_BY = %s,
                                            REVIEW_DATE = %s
                                        WHERE EMPLOYEE_ID = %s
                                    """
                                    cursor.execute(
                                        _emp_update_query,
                                        (
                                            str(item["MANAGER_ID"]),
                                            current_datetime_utc,
                                            item["LAST_UPDATED_BY"],
                                            item["REVIEW_DATE"],
                                            item['EMPLOYEE_ID'],
                                        )
                                    )
                                elif item["ATTRIBUTE1"] == "job":
                                    _emp_update_query = """
                                        UPDATE RAC_FS_TM_EMPLOYEE_DTLS
                                        SET
                                            JOB_ID = %s,
                                            LAST_UPDATE_DATE = %s,
                                            LAST_UPDATED_BY = %s,
                                            REVIEW_DATE = %s
                                        WHERE EMPLOYEE_ID = %s
                                    """
                                    cursor.execute(
                                        _emp_update_query,
                                        (
                                            job_id,
                                            current_datetime_utc,
                                            item["LAST_UPDATED_BY"],
                                            item["REVIEW_DATE"],
                                            item['EMPLOYEE_ID'],
                                        )
                                    )
                                elif item["ATTRIBUTE1"] == "hierarchy":
                                    _emp_update_query = """
                                        UPDATE RAC_FS_TM_EMPLOYEE_DTLS
                                        SET
                                            AREA_ID = %s,
                                            LAST_UPDATE_DATE = %s,
                                            LAST_UPDATED_BY = %s,
                                            REVIEW_DATE = %s
                                        WHERE EMPLOYEE_ID = %s
                                    """
                                    cursor.execute(
                                        _emp_update_query,
                                        (
                                            area_id,
                                            current_datetime_utc,
                                            item["LAST_UPDATED_BY"],
                                            item["REVIEW_DATE"],
                                            item['EMPLOYEE_ID'],
                                        )
                                    )
                                else:
                                    _emp_update_query = """
                                        UPDATE RAC_FS_TM_EMPLOYEE_DTLS
                                        SET
                                            EMPLOYEE_NAME = %s,
                                            AREA_ID = %s,
                                            LOCATION_CODE = %s,
                                            MANAGER_ID = %s,
                                            JOB_ID = %s,
                                            TEAM_TYPE_ID = %s,
                                            WORK_SHIFT = %s,
                                            ON_CALL = %s,
                                            ON_SITE = %s,
                                            DEDICATED = %s,
                                            DEDICATED_TO = %s,
                                            BUSINESS_ORG = %s,
                                            SERVICE_ADVANTAGE = %s,
                                            SERVICE_START_DATE = %s,
                                            SERVICE_END_DATE = %s,
                                            FS_STATUS = %s,
                                            RECORD_COMPLETE = %s,
                                            MANAGER_FLAG = %s,
                                            ADMIN_NOTES = %s,
                                            ALTERNATE_EMAIL = %s,
                                            LAST_UPDATE_DATE = %s,
                                            LAST_UPDATED_BY = %s,
                                            ABSENCE_START_DATE = %s,
                                            ABSENCE_END_DATE = %s,
                                            ACTUAL_RETURN_TO_WORK = %s,
                                            HR_STATUS = %s,
                                            OFSC_STATUS = %s,
                                            PRODUCTION_PRINT = %s,
                                            REVIEW_DATE = %s
                                        WHERE EMPLOYEE_ID = %s
                                    """
                                    cursor.execute(
                                        _emp_update_query,
                                        (
                                            item["EMPLOYEE_NAME"],
                                            area_id,
                                            item["LOC_CODE"],
                                            manager_id_str,
                                            job_id,
                                            team_type_id,
                                            item["WORK_SHIFT"],
                                            item["ON_CALL"],
                                            item["ON_SITE"],
                                            item["DEDICATED"],
                                            item["DEDICATED_TO"],
                                            item["BUSINESS_ORG"],
                                            item["SERVICE_ADVANTAGE"],
                                            item["SERVICE_START_DATE"],
                                            item["SERVICE_END_DATE"],
                                            item["FS_STATUS"],
                                            item["RECORD_COMPLETE"],
                                            item["MANAGER_FLAG"],
                                            item["ADMIN_NOTES"],
                                            item["ALTERNATE_EMAIL"],
                                            current_datetime_utc,
                                            item["LAST_UPDATED_BY"],
                                            item['ABSENCE_START_DATE'],
                                            item['ABSENCE_END_DATE'],
                                            item['ACTUAL_RETURN_TO_WORK'],
                                            item['HR_STATUS'],
                                            item["OFSC_STATUS"],
                                            item["PRODUCTION_PRINT"],
                                            item['REVIEW_DATE'],
                                            item['EMPLOYEE_ID'],
                                        )
                                    )

                                logger.info(
                                    f"_emp_update_query : {_emp_update_query}")

                                update_query = """
                                    UPDATE RAC_FS_TM_EMPLOYEE_UPD
                                    SET
                                        CHANGE_STATUS = 'Processed',
                                        PROCESSED_DATE = %s,
                                        LAST_UPDATE_DATE = %s,
                                        LAST_UPDATED_BY = %s
                                    WHERE CHANGE_ID = %s
                                """
                                cursor.execute(
                                    update_query,
                                    (
                                        current_datetime_utc,
                                        current_datetime_utc,
                                        item["LAST_UPDATED_BY"],
                                        item['CHANGE_ID'],
                                    )
                                )

                                # Commit the changes to the database
                                connection.commit()

                                logger.info(f"update_query : {update_query}")

                                if item["CSA_NOTIFICATION_REQUIRED"] == "Y":
                                    cursor.execute(
                                        "SELECT EMAIL_ID FROM RAC_FS_TM_NOTIF WHERE NOTIFICATION_NAME = 'CSA Notifications' AND STATUS = 'ACTIVE'"
                                    )
                                    res_email_ids = cursor.fetchall()
                                    if res_email_ids:
                                        cursor.execute(
                                            """
                                            SELECT EMP.RESOURCE_NUMBER, EMP.EMPLOYEE_NAME, MGR.EMPLOYEE_NAME as MANAGER_NAME,
                                            MGR.RESOURCE_NUMBER as MANAGER_RESOURCE_NUMBER, EMP.ACTUAL_TERMINATION_DATE,
                                            FS_EMP.HR_STATUS, EMP.EMAIL, MGR.EMAIL AS MANAGER_EMAIL
                                            FROM RAC_FS_TM_EMPLOYEE_UPD FS_EMP
                                            JOIN RAC_HR_TM_EMPLOYEE_DTLS EMP ON EMP.EMPLOYEE_ID = FS_EMP.EMPLOYEE_ID
                                            LEFT JOIN RAC_HR_TM_EMPLOYEE_DTLS MGR ON FS_EMP.MANAGER_ID = MGR.EMPLOYEE_ID
                                            WHERE FS_EMP.CHANGE_ID = %s
                                            """,
                                            (item["CHANGE_ID"],),
                                        )
                                        new_result = cursor.fetchone()
                                        logger.info(
                                            f"new_result : {new_result}")
                                        cursor.execute(
                                            sql_get_name, (item["LAST_UPDATED_BY"],)
                                        )
                                        last_updated_name_new = cursor.fetchone()
                                        cursor.execute(
                                            sql_get_name, (item["APPROVED_BY"],)
                                        )
                                        approved_by_name = cursor.fetchone()
                                        cursor.execute(
                                            sql_get_name, (item["REQUESTED_BY"],)
                                        )
                                        requested_by_name = cursor.fetchone()
                                        new_data = {
                                            "CSA_CHANGE_COMMENT": item["CSA_CHANGE_COMMENT"],
                                            "LAST_UPDATE_DATE": item["LAST_UPDATE_DATE"],
                                            "LAST_UPDATED_BY": last_updated_name_new["USER_NAME"],
                                            "CREATION_DATE": item["CREATION_DATE"],
                                            "CHANGE_TYPE": item["CHANGE_TYPE"],
                                            "EMPLOYEE_ID": item["EMPLOYEE_ID"],
                                            "RESOURCE_NUMBER": new_result["RESOURCE_NUMBER"],
                                            "EMPLOYEE_NAME": new_result["EMPLOYEE_NAME"],
                                            "EMAIL": new_result["EMAIL"],
                                            "FS_STATUS": item["FS_STATUS"],
                                            "REGION": item["REGION"],
                                            "AREA": item["AREA"],
                                            "LOC_CODE": item["LOC_CODE"],
                                            "MANAGER_RESOURCE_NUMBER": new_result["MANAGER_RESOURCE_NUMBER"],
                                            "MANAGER_NAME": new_result["MANAGER_NAME"],
                                            "MANAGER_EMAIL": new_result["MANAGER_EMAIL"],
                                            "AREA_DIR_NAME": hierarchy["EMPLOYEE_NAME"] if hierarchy else None,
                                            "AREA_DIR_EMAIL": hierarchy["EMAIL"] if hierarchy else None,
                                            "TEAM_TYPE": item["TEAM_TYPE"],
                                            "ALTERNATE_EMAIL": item["ALTERNATE_EMAIL"],
                                            "JOB_TITLE": item["JOB_TITLE"],
                                            "ACTUAL_TERMINATION_DATE": new_result["ACTUAL_TERMINATION_DATE"],
                                            "APPROVED_BY": approved_by_name["USER_NAME"],
                                            "CHANGE_NOTE": item["CHANGE_NOTE"],
                                            "HR_STATUS": new_result["HR_STATUS"],
                                            "REQUESTED_BY": requested_by_name["USER_NAME"],
                                            "ABSENCE_START_DATE": item["ABSENCE_START_DATE"],
                                            "ABSENCE_END_DATE": item["ABSENCE_END_DATE"],
                                        }
                                        logger.info(f"new_data : {new_data}")
                                        recipient_email = [
                                            (res["EMAIL_ID"]) for res in res_email_ids]
                                        logger.info(
                                            f"recipient_email : {recipient_email}")
                                        subject = f"Techmaster Changes for Employee {new_result['EMPLOYEE_NAME']} {current_date}. Area: {item['AREA']}"
                                        # adding 4 sec delay
                                        time.sleep(4)
                                        # Send the CSA email notification
                                        send_email_csa(
                                            recipient_email, old_data, new_data, subject)
                                        print("csa email send")
                                        update_query = """
                                            UPDATE RAC_FS_TM_EMPLOYEE_UPD
                                            SET
                                                CSA_NOTIFICATION_COMPLETE = 'Y'
                                            WHERE CHANGE_ID = %s
                                        """
                                        cursor.execute(
                                            update_query,
                                            (
                                                item['CHANGE_ID'],
                                            )
                                        )

                                        # Commit the changes to the database
                                        connection.commit()

                                        logger.info(
                                            f"update_query : {update_query}")
                            else:
                                logging.warning(
                                    "No employee record found for EMPLOYEE_ID: %s", item['EMPLOYEE_ID'])

                        else:
                            logging.warning(
                                "No employee record found for EMPLOYEE_ID: %s", item['EMPLOYEE_ID'])
                    except Exception as inner_exception:
                        logging.error("Error processing employee ID %s: %s",
                                      item['EMPLOYEE_ID'], str(inner_exception))

        else:
            logging.warning("No records found in approved notification")

    except Exception as e:
        logging.error("Error in Approved Notification: %s", str(e))
    finally:
        if connection:
            connection.close()


def PROCESSED_MANAGER_TRANSFER_NOTIFICATION_RECORDS(**kwargs):
    try:
        connection = DatabaseConnection().connect()
        records = get_manager_transfer_records()
        # ATTRIBUTE2 store old manager id
        if records:
            with connection.cursor() as cursor:
                for item in records:
                    cursor.execute(
                        "SELECT * FROM RAC_FS_TM_EMPLOYEE_DTLS WHERE EMPLOYEE_ID = %s", (item['EMPLOYEE_ID'],))
                    emp_update_query = cursor.fetchone()

                    sql_get_name = """ SELECT RAC_FS_TM_GET_USER_NAME (%s) AS USER_NAME """

                    if emp_update_query:
                        employee_id = emp_update_query['EMPLOYEE_ID']

                        # get hierarchy info
                        hierarchy = get_area_dir_info(employee_id)

                        sql_query = """
                            SELECT EMP.RESOURCE_NUMBER, FS_EMP.EMPLOYEE_NAME, REGION.REGION_NAME,
                            AREA.AREA_SHORT_NAME, MGR.EMPLOYEE_NAME AS MANAGER_NAME,
                            MGR.RESOURCE_NUMBER AS MANAGER_RESOURCE_NUMBER, TEAM.TEAM_TYPE_NAME,
                            JOB.JOB_TITLE, EMP.ACTUAL_TERMINATION_DATE, FS_EMP.HR_STATUS, EMP.EMAIL, FS_EMP.SERVICE_END_DATE
                            FROM RAC_FS_TM_EMPLOYEE_DTLS FS_EMP
                            JOIN RAC_HR_TM_EMPLOYEE_DTLS EMP ON EMP.EMPLOYEE_ID = FS_EMP.EMPLOYEE_ID
                            JOIN RAC_HR_TM_EMPLOYEE_DTLS MGR ON FS_EMP.MANAGER_ID = MGR.EMPLOYEE_ID
                            JOIN RAC_FS_TM_AREA AREA ON AREA.AREA_ID = FS_EMP.AREA_ID
                            JOIN RAC_FS_TM_REGION REGION ON REGION.REGION_ID = AREA.REGION_ID
                            LEFT JOIN RAC_FS_TM_TEAM_TYPE TEAM ON TEAM.TEAM_TYPE_ID = FS_EMP.TEAM_TYPE_ID
                            LEFT JOIN RAC_FS_TM_JOB_CODE JOB ON JOB.JOB_ID = FS_EMP.JOB_ID
                            WHERE FS_EMP.EMPLOYEE_ID = %s
                        """
                        cursor.execute(sql_query, (item['EMPLOYEE_ID'],))
                        old_result = cursor.fetchone()
                        if old_result:
                            sql_query = """
                                select b.EMAIL AS MANAGER_EMAIL, b.EMPLOYEE_NAME AS MANAGER_NAME, b.RESOURCE_NUMBER AS MANAGER_RESOURCE_NUMBER 
                                from RAC_FS_TM_EMPLOYEE_DTLS as a inner join
                                RAC_HR_TM_EMPLOYEE_DTLS as b on a.EMPLOYEE_ID = b.EMPLOYEE_ID 
                                where a.EMPLOYEE_ID  = %s
                            """
                            cursor.execute(sql_query, (item['ATTRIBUTE2'],))
                            manager_Info = cursor.fetchone()
                            cursor.execute(
                                sql_get_name, (
                                    emp_update_query["LAST_UPDATED_BY"],)
                            )
                            last_updated_name = cursor.fetchone()
                            old_data = {
                                "CSA_CHANGE_COMMENT": None,
                                "LAST_UPDATE_DATE": emp_update_query["LAST_UPDATE_DATE"],
                                "LAST_UPDATED_BY": last_updated_name["USER_NAME"],
                                "CREATION_DATE": emp_update_query["CREATION_DATE"],
                                "CHANGE_TYPE": None,
                                "EMPLOYEE_ID": emp_update_query["EMPLOYEE_ID"],
                                "RESOURCE_NUMBER": old_result["RESOURCE_NUMBER"],
                                "EMPLOYEE_NAME": old_result["EMPLOYEE_NAME"],
                                "EMAIL": old_result["EMAIL"],
                                "FS_STATUS": emp_update_query["FS_STATUS"],
                                "REGION": old_result["REGION_NAME"],
                                "AREA": old_result["AREA_SHORT_NAME"],
                                "LOC_CODE": emp_update_query["LOCATION_CODE"],
                                "MANAGER_RESOURCE_NUMBER": manager_Info["MANAGER_RESOURCE_NUMBER"] if manager_Info else None,
                                "MANAGER_NAME": manager_Info["MANAGER_NAME"] if manager_Info else None,
                                "MANAGER_EMAIL": manager_Info["MANAGER_EMAIL"] if manager_Info else None,
                                "AREA_DIR_NAME": hierarchy["EMPLOYEE_NAME"] if hierarchy else None,
                                "AREA_DIR_EMAIL": hierarchy["EMAIL"] if hierarchy else None,
                                "TEAM_TYPE": old_result["TEAM_TYPE_NAME"],
                                "ALTERNATE_EMAIL": emp_update_query["ALTERNATE_EMAIL"],
                                "JOB_TITLE": old_result["JOB_TITLE"],
                                "ACTUAL_TERMINATION_DATE": None,
                                "APPROVED_BY": None,
                                "CHANGE_NOTE": None,
                                "HR_STATUS": old_result["HR_STATUS"],
                                "REQUESTED_BY": None,
                                "ABSENCE_START_DATE": emp_update_query["ABSENCE_START_DATE"],
                                "ABSENCE_END_DATE": emp_update_query["ABSENCE_END_DATE"],
                            }

                            # Get new manager email ID and send the data
                            cursor.execute(
                                "SELECT EMAIL FROM RAC_HR_TM_EMPLOYEE_DTLS where EMPLOYEE_ID = %s", (item['ATTRIBUTE2'],))
                            res_email_ids = cursor.fetchall()
                            if res_email_ids:
                                cursor.execute(
                                    """
                                    SELECT EMP.RESOURCE_NUMBER, EMP.EMPLOYEE_NAME, MGR.EMPLOYEE_NAME as MANAGER_NAME,
                                    MGR.RESOURCE_NUMBER as MANAGER_RESOURCE_NUMBER, EMP.ACTUAL_TERMINATION_DATE,
                                    EMP.HR_STATUS, EMP.EMAIL, MGR.EMAIL AS MANAGER_EMAIL
                                    FROM RAC_FS_TM_EMPLOYEE_UPD FS_EMP
                                    JOIN RAC_HR_TM_EMPLOYEE_DTLS EMP ON EMP.EMPLOYEE_ID = FS_EMP.EMPLOYEE_ID
                                    JOIN RAC_HR_TM_EMPLOYEE_DTLS MGR ON FS_EMP.MANAGER_ID = MGR.EMPLOYEE_ID
                                    WHERE FS_EMP.CHANGE_ID = %s
                                    """,
                                    (item["CHANGE_ID"],),
                                )
                                new_result = cursor.fetchone()
                                logger.info(f"new_result : {new_result}")
                                cursor.execute(
                                    sql_get_name, (item["LAST_UPDATED_BY"],)
                                )
                                last_updated_name_new = cursor.fetchone()
                                cursor.execute(
                                    sql_get_name, (item["APPROVED_BY"],)
                                )
                                approved_by_name = cursor.fetchone()
                                cursor.execute(
                                    sql_get_name, (item["REQUESTED_BY"],)
                                )
                                requested_by_name = cursor.fetchone()
                                new_data = {
                                    "CSA_CHANGE_COMMENT": item["CSA_CHANGE_COMMENT"],
                                    "LAST_UPDATE_DATE": item["LAST_UPDATE_DATE"],
                                    "LAST_UPDATED_BY": last_updated_name_new["USER_NAME"],
                                    "CREATION_DATE": item["CREATION_DATE"],
                                    "CHANGE_TYPE": item["CHANGE_TYPE"],
                                    "EMPLOYEE_ID": item["EMPLOYEE_ID"],
                                    "RESOURCE_NUMBER": new_result["RESOURCE_NUMBER"],
                                    "EMPLOYEE_NAME": new_result["EMPLOYEE_NAME"],
                                    "EMAIL": new_result["EMAIL"],
                                    "FS_STATUS": item["FS_STATUS"],
                                    "REGION": item["REGION"],
                                    "AREA": item["AREA"],
                                    "LOC_CODE": item["LOC_CODE"],
                                    "MANAGER_RESOURCE_NUMBER": new_result["MANAGER_RESOURCE_NUMBER"],
                                    "MANAGER_NAME": new_result["MANAGER_NAME"],
                                    "MANAGER_EMAIL": new_result["MANAGER_EMAIL"],
                                    "AREA_DIR_NAME": hierarchy["EMPLOYEE_NAME"] if hierarchy else None,
                                    "AREA_DIR_EMAIL": hierarchy["EMAIL"] if hierarchy else None,
                                    "TEAM_TYPE": item["TEAM_TYPE"],
                                    "ALTERNATE_EMAIL": item["ALTERNATE_EMAIL"],
                                    "JOB_TITLE": item["JOB_TITLE"],
                                    "ACTUAL_TERMINATION_DATE": new_result["ACTUAL_TERMINATION_DATE"],
                                    "APPROVED_BY": approved_by_name["USER_NAME"],
                                    "CHANGE_NOTE": item["CHANGE_NOTE"],
                                    "HR_STATUS": item["HR_STATUS"],
                                    "REQUESTED_BY": requested_by_name["USER_NAME"],
                                    "ABSENCE_START_DATE": emp_update_query["ABSENCE_START_DATE"],
                                    "ABSENCE_END_DATE": emp_update_query["ABSENCE_END_DATE"],
                                }
                                logger.info(f"new_data : {new_data}")
                                old_manager_recipient_email = [
                                    (res["EMAIL"]) for res in res_email_ids]
                                logger.info(
                                    f"old_manager_recipient_email : {old_manager_recipient_email}")
                                # Send the email notification to old manager
                                subject = f"Techmaster Changes for {old_result['MANAGER_NAME']}"
                                send_email_csa(
                                    old_manager_recipient_email, old_data, new_data, subject)

                                cursor.execute(
                                    "SELECT EMAIL FROM RAC_HR_TM_EMPLOYEE_DTLS where EMPLOYEE_ID = %s", (item['MANAGER_ID'],))
                                new_email = cursor.fetchall()
                                new_manager_recipient_email = [
                                    (res["EMAIL"]) for res in new_email]
                                logger.info(
                                    f"new_manager_recipient_email : {new_manager_recipient_email}")
                                # Send the email notification to new manager
                                subject = f"Techmaster Changes for {new_result['MANAGER_NAME']}"
                                send_email_csa(
                                    new_manager_recipient_email, old_data, new_data, subject)
                                print("csa email send")
                                update_query = """
                                    UPDATE RAC_FS_TM_EMPLOYEE_UPD
                                    SET
                                        ATTRIBUTE3 = 'SEND'
                                    WHERE CHANGE_ID = %s
                                """
                                cursor.execute(
                                    update_query,
                                    (
                                        item['CHANGE_ID'],
                                    )
                                )

                                # Commit the changes to the database
                                connection.commit()

                                logger.info(f"update_query : {update_query}")
                        else:
                            logging.warning(
                                "No employee record found for EMPLOYEE_ID: %s", item['ATTRIBUTE2'])

                    else:
                        logging.warning(
                            "No employee record found for EMPLOYEE_ID: %s", item['EMPLOYEE_ID'])
        else:
            logging.warning(
                "No records found in manager transfer notification")

    except Exception as e:
        logging.error("Error in manager transfer Notification: %s", str(e))
    finally:
        if connection:
            connection.close()

# Implement a PythonOperator for invoking a Lambda function
def invoke_lambda_function(**context):
    try:
        lambda_client = boto3.client('lambda')
        response_1 = lambda_client.invoke(
            FunctionName='RAC-PSIRITEM-CSV-XLS-UAT', InvocationType='RequestResponse')
        logger.info('Lambda Function Response: %s', response_1)
    except Exception as e:
        logger.error('Error invoking Lambda function: %s', str(e))


# Define a DummyOperator for the exit task
t2 = DummyOperator(
    task_id='Exit_Task',
    dag=dag
)

# Define PythonOperators for different tasks
RAC_DAILY_LAST_24_HRS_RECORDS_NOTIFICATION = PythonOperator(
    task_id='RAC_DAILY_LAST_24_HRS_RECORDS_NOTIFICATION',
    python_callable=DAILY_LAST_24_HRS_RECORDS_NOTIFICATION,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_PENDING_RECORDS_NOTIFICATION = PythonOperator(
    task_id='RAC_PENDING_RECORDS_NOTIFICATION',
    python_callable=DAILY_NOTIFICATION_PENDING_RECORDS,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_CSA_APPROVED_NOTIFICATION = PythonOperator(
    task_id='RAC_CSA_APPROVED_NOTIFICATION',
    python_callable=CSA_NOTIFICATION_APPROVED_RECORDS,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_PROCESSED_RECORDS_NOTIFICATION_TO_MANAGER = PythonOperator(
    task_id='RAC_PROCESSED_RECORDS_NOTIFICATION_TO_MANAGER',
    python_callable=DAILY_PROCESSED_RECORDS_NOTIFICATION_TO_MANAGER,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_PROCESSED_MANAGER_TRANSFER_NOTIFICATION = PythonOperator(
    task_id='RAC_PROCESSED_MANAGER_TRANSFER_NOTIFICATION',
    python_callable=PROCESSED_MANAGER_TRANSFER_NOTIFICATION_RECORDS,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_INCOMPLETED_RECORD_NOTIFICATION = PythonOperator(
    task_id='RAC_INCOMPLETED_RECORD_NOTIFICATION',
    python_callable=INCOMPLETED_RECORD_NOTIFICATION,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_DAILY_LAST_24_HRS_RECORDS_NOTIFICATION \
    >> RAC_PENDING_RECORDS_NOTIFICATION \
    >> RAC_CSA_APPROVED_NOTIFICATION \
    >> RAC_PROCESSED_RECORDS_NOTIFICATION_TO_MANAGER \
    >> RAC_PROCESSED_MANAGER_TRANSFER_NOTIFICATION \
    >> RAC_INCOMPLETED_RECORD_NOTIFICATION \
    >> t2
