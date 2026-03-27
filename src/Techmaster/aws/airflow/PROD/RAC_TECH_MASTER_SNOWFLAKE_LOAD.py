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

# Set the DAG to use UTC timezone
# local_tz = pendulum.timezone("UTC")

DAG_NAME = 'RAC_TECH_MASTER_SNOWFLAKE_LOAD'

current_datetime_utc = datetime.now(local_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
formatted_current_datetime_utc = datetime.now(
    local_tz).strftime('%Y-%m-%d %H:%M:%S')
current_date = datetime.now(local_tz).strftime('%Y-%m-%d')
# Set the start date to 7 AM EST
start_date = datetime(2023, 10, 25, 7, 0, 0, tzinfo=local_tz)

default_args = {
    'owner': 'Airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id=DAG_NAME,
    default_args=default_args,
    # This triggers the DAG daily at 7 AM US/Eastern time
    schedule_interval='0 7 * * *',
    catchup=False,
)

AWS_SECRETS_MYSQL = Variable.get('AWS_SECRETS_MYSQL')
SMTP_SERVER = Variable.get('SMTP_SERVER')
FROM_ADDRESS = Variable.get('FROM_ADDRESS')
AWS_SECRETS_S3 = Variable.get('AWS_SECRETS_S3')
IICS_USER_NAME = Variable.get('IICS_USER_NAME')
IICS_PASSWORD = Variable.get('IICS_PASSWORD')
TECH_MASTER_ENV = Variable.get('TECH_MASTER_ENV')

TECH_MASTER_S3_BUCKET = Variable.get('TECH_MASTER_S3_BUCKET')
TECH_MASTER_SNOWFLAKE_S3_BUCKET = Variable.get(
    'TECH_MASTER_SNOWFLAKE_S3_BUCKET')
S3_EXPORT_SNOWFLAKE_DAILY_KEY_PATH = Variable.get(
    'S3_EXPORT_SNOWFLAKE_DAILY_KEY_PATH')
S3_EXPORT_SNOWFLAKE_MONTHLY_OLD_FORMAT_KEY_PATH = Variable.get(
    'S3_EXPORT_SNOWFLAKE_MONTHLY_OLD_FORMAT_KEY_PATH')
S3_EXPORT_SNOWFLAKE_MONTHLY_NEW_FORMAT_KEY_PATH = Variable.get(
    'S3_EXPORT_SNOWFLAKE_MONTHLY_NEW_FORMAT_KEY_PATH')
SF_S3_EXPORT_SNOWFLAKE_DAILY_KEY_PATH = Variable.get(
    'SF_S3_EXPORT_SNOWFLAKE_DAILY_KEY_PATH')
SF_S3_EXPORT_SNOWFLAKE_MONTHLY_OLD_FORMAT_KEY_PATH = Variable.get(
    'SF_S3_EXPORT_SNOWFLAKE_MONTHLY_OLD_FORMAT_KEY_PATH')
SF_S3_EXPORT_SNOWFLAKE_MONTHLY_NEW_FORMAT_KEY_PATH = Variable.get(
    'SF_S3_EXPORT_SNOWFLAKE_MONTHLY_NEW_FORMAT_KEY_PATH')


session = requests.post(
    url='https://dm-us.informaticacloud.com/ma/api/v2/user/login',
    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    json={'@type': 'login', 'username': IICS_USER_NAME, 'password': IICS_PASSWORD}
)

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

def upload_csv_to_s3(csv_file, s3_bucket, s3_key):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(csv_file, s3_bucket, s3_key)
        logging.info(
            f"Uploaded {csv_file} to S3 bucket {s3_bucket} with key {s3_key}")
    except Exception as e:
        logging.error(f"Error uploading {csv_file} to S3: {str(e)}")


# Snowflake

def create_snowflake_csv_from_daily_records(records):
    csv_file = '/tmp/snowflake_data.csv'
    fieldnames = ['MSTTL_DATES', 'MSTTL_EMPLOYEE_ID', 'MSTTL_RESOURCE_NUMBER', 'MSTTL_RECORD_COMPLETE', 'MSTTL_CONTINGENT_WORKER',
                  'MSTTL_EMPLOYEE_NAME', 'MSTTL_EMPLOYEE_EMAIL', 'MSTTL_ADDITIONAL_EMPLOYEE_EMAIL', 'MSTTL_EBS_USER_NAME',
                  'MSTTL_FS_STATUS', 'MSTTL_BUSINESS_ORG', 'MSTTL_JOB_TITLE', 'MSTTL_JOB_TYPE', 'MSTTL_MANAGER_FLAG', 'MSTTL_JOB_ADP_CODE',
                  'MSTTL_JOB_MATCH_TO_HR', 'MSTTL_TEAM_TYPE', 'MSTTL_OFSC_PRODUCTION_PRINT', 'MSTTL_REGION', 'MSTTL_AREA_SHORT',
                  'MSTTL_LOCATION_CODE', 'MSTTL_REGION_AND_AREA_MATCH_TO_HR', 'MSTTL_MANAGER_NAME', 'MSTTL_MANAGER_EMPLOYEE_ID',
                  'MSTTL_MANAGER_RESOURCE_NUM', 'MSTTL_MANAGER_EMAIL', 'MSTTL_MANAGER_MATCH_TO_HR', 'MSTTL_HR_STATUS', 'MSTTL_LAST_HIRE_DATE',
                  'MSTTL_SERVICE_START_DATE', 'MSTTL_SERVICE_END_DATE', 'MSTTL_ACTUAL_TERMINATION_DATE', 'MSTTL_ABSENCE_START_DATE',
                  'MSTTL_ABSENCE_END_DATE', 'MSTTL_ACTUAL_RETURN_TO_WORK', 'MSTTL_WORK_SHIFT_1ST_2ND_3RD', 'MSTTL_ON_CALL', 'MSTTL_ON_SITE',
                  'MSTTL_DEDICATED', 'MSTTL_DEDICATED_TO', 'MSTTL_SERVICE_ADVANTAGE', 'MSTTL_REGION_DIR_NAME', 'MSTTL_REGION_DIR_EMPLOYEE_ID',
                  'MSTTL_REGION_DIR_RESOURCE_NUM', 'MSTTL_REGION_DIR_EMAIL', 'MSTTL_AREA_DIR_NAME', 'MSTTL_AREA_DIR_EMPLOYEE_ID',
                  'MSTTL_AREA_DIR_RESOURCE_NUMBER', 'MSTTL_AREA_DIR_EMAIL', 'MSTTL_AREA_FOM_NAME', 'MSTTL_AREA_FOM_EMPLOYEE_ID',
                  'MSTTL_AREA_FOM_RESOURCE_NUMBER', 'MSTTL_AREA_FOM_EMAIL', 'MSTTL_CHANGE_NOTE', 'MSTTL_CHANGE_EFFECTIVE_DATE',
                  'MSTTL_ADMIN_NOTES', 'MSTTL_REVIEW_DATE', 'MSTTL_UPDATE_FLAG', 'MSTTL_LAST_UPDATE_DATE']

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow({field: record.get(field, '')
                            for field in fieldnames})
    return csv_file


def create_snowflake_csv_from_monthly_records_old_format(records):
    csv_file = '/tmp/snowflake_monthly_data_old_format.csv'
    fieldnames = ['MSTTLTL_SNAPSHOT_DATE', 'MSTTL_FSMID', 'MSTTL_REGID', 'MSTTL_MKTID', 'MSTTL_REGION',
                  'MSTTL_OLD_REGION', 'MSTTL_OLD_AREANAME', 'MSTTL_AREANAME', 'MSTTL_AREA', 'MSTTL_BRANCH',
                  'MSTTL_TEAM', 'MSTTL_RBS_IKON', 'MSTTL_TECHID', 'MSTTL_EMP_NUM',
                  'MSTTL_TECHNAME', 'MSTTL_JOB_TITLE', 'MSTTL_JOB_TITLE_SHORTNAME', 'MSTTL_TECH_EMAIL', 'MSTTL_TECH_CELL',
                  'MSTTL_CELL_FORMAT', 'MSTTL_ALTSURVEYCONTACT', 'MSTTL_ALTSURVEYEMAIL', 'MSTTL_TECH_PAGER', 'MSTTL_TERRITORY_TYPE', 'MSTTL_FSM',
                  'MSTTL_FSM_EMAIL', 'MSTTL_FSM_RESOURCE_NUMBER', 'MSTTL_FSM_EMPID', 'MSTTL_TRAINING_ID', 'MSTTL_UPDATE',
                  'MSTTL_FTE', 'MSTTL_TERMED_Y_N', 'MSTTL_TERMED_DATE', 'MSTTL_HIRE_DATE', 'MSTTL_OTHER', 'MSTTL_CHANGE',
                  'MSTTL_DISTRICT_DIR', 'MSTTL_DISTRICT_DIR_EMAIL', 'MSTTL_DISTRICT_DIR_RESOURCE_NBR', 'MSTTL_DISTRICT_DIR_EMPLOYEEID',
                  'MSTTL_DISTRICT_OPS', 'MSTTL_DISTRICT_OPS_EMAIL', 'MSTTL_DISTRICT_OPS_RESOURCE_NBR', 'MSTTL_DISTRICT_OPS_EMPLOYEEID',
                  'MSTTL_DIRECTOR', 'MSTTL_DIRECTOR_EMAIL', 'MSTTL_DIRECTOR_RESOURCE_NBR', 'MSTTL_DIRECTOR_EMPLOYEEID', 'MSTTL_AREAOPS',
                  'MSTTL_AREAOPS_EMAIL', 'MSTTL_AREAOPS_RESOURCE', 'MSTTL_AREAOPS_EMPLOYEEID', 'MSTTL_TECHADS',
                  'MSTTL_LEAD_TECH_RESOURCE_NUMBER', 'MSTTL_LEAD_TECH_RESOURCE_NAME', 'MSTTL_LEAD_TECH_CELL_NUMBER', 'MSTTL_PAGER_FORMAT',
                  'MSTTL_EDGE', 'MSTTL_PLATFORM', 'MSTTL_BRANCHLOCATION', 'MSTTL_JOB_CODE', 'MSTTL_JOB_TYPE', 'MSTTL_DROPSITE',
                  'MSTTL_DROPSITEADD', 'MSTTL_DROPSITECOUNTY', 'MSTTL_SUBACCT', 'MSTTL_R12_BRANCH_LOCATION', 'MSTTL_TERRITORY_METHOD',
                  'MSTTL_CSA_EMAIL', 'MSTTL_CSA_DL_EMAIL', 'MSTTL_EXCESS_CALL_LOAD', 'MSTTL_CALL_LOAD_NOTIFICATION', 'MSTTL_IKON1_USERNAME',
                  'MSTTL_DROPSITE2', 'MSTTL_DROPSITEADD2', 'MSTTL_DROPSITECOUNTY2', 'MSTTL_SUBACCT2', 'MSTTL_DROPSITE3',
                  'MSTTL_DROPSITEADD3', 'MSTTL_DROPSITECOUNTY3', 'MSTTL_SUBACCT3', 'MSTTL_TERRITORYMAKEUP', 'MSTTL_ALLOWDRUMS',
                  'MSTTL_ALLOWPCB', 'MSTTL_ALLOWSUPPLIES', 'MSTTL_LOCATION_CODE', 'MSTTL_SALES_MARKETPLACE', 'MSTTL_SALES_DISTRICT',
                  'MSTTL_UPDATED', 'MSTTL_BUSINESS_TYPE']

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow({field: record.get(field, '')
                            for field in fieldnames})
    return csv_file


def create_snowflake_csv_from_monthly_records_new_format(records):
    csv_file = '/tmp/snowflake_monthly_data_new_format.csv'
    fieldnames = [
                    'MSTTL_DATES', 'MSTTL_EMPLOYEE_ID', 'MSTTL_RESOURCE_NUMBER', 'MSTTL_RECORD_COMPLETE', 'MSTTL_CONTINGENT_WORKER',
                    'MSTTL_EMPLOYEE_NAME', 'MSTTL_EMPLOYEE_EMAIL', 'MSTTL_ADDITIONAL_EMPLOYEE_EMAIL', 'MSTTL_EBS_USER_NAME',
                    'MSTTL_FS_STATUS', 'MSTTL_BUSINESS_ORG', 'MSTTL_JOB_TITLE', 'MSTTL_JOB_TYPE', 'MSTTL_MANAGER_FLAG',
                    'MSTTL_JOB_ADP_CODE', 'MSTTL_JOB_MATCH_TO_HR', 'MSTTL_TEAM_TYPE', 'MSTTL_OFSC_PRODUCTION_PRINT',
                    'MSTTL_REGION', 'MSTTL_AREA_SHORT', 'MSTTL_LOCATION_CODE', 'MSTTL_REGION_AND_AREA_MATCH_TO_HR',
                    'MSTTL_MANAGER_NAME', 'MSTTL_MANAGER_EMPLOYEE_ID', 'MSTTL_MANAGER_RESOURCE_NUM', 'MSTTL_MANAGER_EMAIL', 'MSTTL_MANAGER_MATCH_TO_HR',
                    'MSTTL_HR_STATUS', 'MSTTL_LAST_HIRE_DATE', 'MSTTL_SERVICE_START_DATE', 'MSTTL_SERVICE_END_DATE',
                    'MSTTL_ACTUAL_TERMINATION_DATE', 'MSTTL_ABSENCE_START_DATE', 'MSTTL_ABSENCE_END_DATE',
                    'MSTTL_ACTUAL_RETURN_TO_WORK', 'MSTTL_WORK_SHIFT_1ST_2ND_3RD', 'MSTTL_ON_CALL', 'MSTTL_ON_SITE',
                    'MSTTL_DEDICATED', 'MSTTL_DEDICATED_TO', 'MSTTL_SERVICE_ADVANTAGE', 'MSTTL_REGION_DIR_NAME',
                    'MSTTL_REGION_DIR_EMPLOYEE_ID', 'MSTTL_REGION_DIR_RESOURCE_NUM', 'MSTTL_REGION_DIR_EMAIL',
                    'MSTTL_AREA_DIR_NAME', 'MSTTL_AREA_DIR_EMPLOYEE_ID', 'MSTTL_AREA_DIR_RESOURCE_NUMBER',
                    'MSTTL_AREA_DIR_EMAIL', 'MSTTL_AREA_FOM_NAME', 'MSTTL_AREA_FOM_EMPLOYEE_ID',
                    'MSTTL_AREA_FOM_RESOURCE_NUMBER', 'MSTTL_AREA_FOM_EMAIL', 'MSTTL_CHANGE_NOTE',
                    'MSTTL_CHANGE_EFFECTIVE_DATE', 'MSTTL_ADMIN_NOTES', 'MSTTL_REVIEW_DATE', 'MSTTL_UPDATE_FLAG',
                    'MSTTL_LAST_UPDATE_DATE'
                ]



    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow({field: record.get(field, '')
                            for field in fieldnames})
    return csv_file


def snowflake_daily_records():

    query = """
        SELECT
            CAST(current_date AS CHAR) AS MSTTL_DATES,
            fs.employee_id AS MSTTL_EMPLOYEE_ID,
            hr.resource_number AS MSTTL_RESOURCE_NUMBER,
            fs.record_complete AS MSTTL_RECORD_COMPLETE,
            hr.contingent_Worker AS MSTTL_CONTINGENT_WORKER,
            hr.employee_name AS MSTTL_EMPLOYEE_NAME,
            hr.email AS MSTTL_EMPLOYEE_EMAIL,
            fs.alternate_email AS MSTTL_ADDITIONAL_EMPLOYEE_EMAIL,
            hr.ebs_user_name AS MSTTL_EBS_USER_NAME,
            fs.fs_status AS MSTTL_FS_STATUS,
            fs.business_org AS MSTTL_BUSINESS_ORG,
            (SELECT job.job_title FROM RAC_FS_TM_JOB_CODE job WHERE fs.job_id = job.job_id) AS MSTTL_JOB_TITLE,
            (SELECT job.job_type FROM RAC_FS_TM_JOB_CODE job WHERE fs.job_id = job.job_id) AS MSTTL_JOB_TYPE,
            fs.manager_flag AS MSTTL_MANAGER_FLAG,
            (SELECT job.job_adp_code FROM RAC_FS_TM_JOB_CODE job WHERE fs.job_id = job.job_id) AS MSTTL_JOB_ADP_CODE,
            CASE WHEN (hr.JOB_TITLE != jc.JOB_TITLE OR hr.JOB_ADP != jc.JOB_ADP_CODE) THEN 'No' ELSE 'Yes' END AS MSTTL_JOB_MATCH_TO_HR,
            (SELECT team.team_type_name FROM RAC_FS_TM_TEAM_TYPE team WHERE fs.team_type_id = team.team_type_id) AS MSTTL_TEAM_TYPE,
            fs.production_print AS MSTTL_OFSC_PRODUCTION_PRINT,
            region.REGION_NAME AS MSTTL_REGION,
            area.AREA_SHORT_NAME AS MSTTL_AREA_SHORT,
            hr.location_code AS MSTTL_LOCATION_CODE,
            CASE WHEN (area_mgr.AREA_SHORT_NAME != area.AREA_SHORT_NAME OR region_mgr.REGION_NAME != region.REGION_NAME) THEN 'No' ELSE 'Yes' END AS MSTTL_REGION_AND_AREA_MATCH_TO_HR,
            fs_mgr.employee_name AS MSTTL_MANAGER_NAME,
            fs_mgr.employee_id AS MSTTL_MANAGER_EMPLOYEE_ID,
            hrm.resource_number AS MSTTL_MANAGER_RESOURCE_NUM,
            hrm.email AS MSTTL_MANAGER_EMAIL,
            CASE WHEN hr.MANAGER_EMPLOYEE_ID = fs.MANAGER_ID THEN 'Yes' ELSE 'No' END AS MSTTL_MANAGER_MATCH_TO_HR,
            fs.hr_status AS MSTTL_HR_STATUS,
            hr.last_hire_date AS MSTTL_LAST_HIRE_DATE,
            fs.service_start_date AS MSTTL_SERVICE_START_DATE,
            fs.service_end_date AS MSTTL_SERVICE_END_DATE,
            hr.actual_termination_date AS MSTTL_ACTUAL_TERMINATION_DATE,
            fs.absence_start_date AS MSTTL_ABSENCE_START_DATE,
            fs.absence_end_date AS MSTTL_ABSENCE_END_DATE,
            fs.actual_return_to_work AS MSTTL_ACTUAL_RETURN_TO_WORK,
            fs.work_shift AS MSTTL_WORK_SHIFT_1ST_2ND_3RD,
            fs.on_call AS MSTTL_ON_CALL,
            fs.on_site AS MSTTL_ON_SITE,
            fs.dedicated AS MSTTL_DEDICATED,
            fs.dedicated_to AS MSTTL_DEDICATED_TO,
            fs.service_advantage AS MSTTL_SERVICE_ADVANTAGE,
            (SELECT employee_name FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_NAME,
            (SELECT employee_id FROM RAC_FS_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_EMPLOYEE_ID,
            (SELECT resource_number FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_RESOURCE_NUM,
            (SELECT email FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_EMAIL,
            (SELECT employee_name FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_NAME,
            (SELECT employee_id FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_EMPLOYEE_ID,
            (SELECT RESOURCE_NUMBER FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_RESOURCE_NUMBER,
            (SELECT email FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_EMAIL,
            (SELECT employee_name FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_NAME,
            (SELECT employee_id FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_EMPLOYEE_ID,
            (SELECT RESOURCE_NUMBER FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_RESOURCE_NUMBER,
            (SELECT email FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_EMAIL,
            (SELECT change_note FROM RAC_FS_TM_EMPLOYEE_UPD up WHERE up.employee_id = fs.employee_id AND up.change_status ='Processed' ORDER BY change_id DESC LIMIT 1 ) AS MSTTL_CHANGE_NOTE,
            (SELECT change_effective_date FROM RAC_FS_TM_EMPLOYEE_UPD up WHERE up.employee_id = fs.employee_id AND up.change_status ='Processed' ORDER BY change_id DESC LIMIT 1 ) AS MSTTL_CHANGE_EFFECTIVE_DATE,
            fs.admin_notes AS MSTTL_ADMIN_NOTES,
            fs.review_date AS MSTTL_REVIEW_DATE,
            NULL AS MSTTL_UPDATE_FLAG,
            fs.last_update_date AS MSTTL_LAST_UPDATE_DATE
        FROM
            RAC_FS_TM_EMPLOYEE_DTLS fs
        LEFT OUTER JOIN
            RAC_HR_TM_EMPLOYEE_DTLS hr ON fs.employee_id = hr.employee_id
        LEFT OUTER JOIN
            RAC_HR_TM_EMPLOYEE_DTLS hrm ON hrm.employee_id = fs.manager_id
        LEFT OUTER JOIN
            RAC_FS_TM_JOB_CODE jc ON jc.JOB_ID = fs.JOB_ID
        LEFT OUTER JOIN
            RAC_FS_TM_EMPLOYEE_DTLS fs_mgr ON fs_mgr.employee_id = fs.manager_id
        LEFT OUTER JOIN
            RAC_FS_TM_AREA AS area ON area.AREA_ID = fs.AREA_ID
        LEFT OUTER JOIN
            RAC_FS_TM_REGION AS region ON region.REGION_ID = area.REGION_ID
        LEFT OUTER JOIN
            RAC_FS_TM_AREA AS area_mgr ON area_mgr.AREA_ID = fs_mgr.AREA_ID
        LEFT OUTER JOIN
            RAC_FS_TM_REGION AS region_mgr ON region_mgr.REGION_ID = area_mgr.REGION_ID

    """
    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            connection.close()
            return records
        return records
    except Exception as e:
        print(str(e), "snowflake_records")
        logging.info('Error snowflake_records from the database: %s', str(e))
        connection.close()
        return None


def snowflake_monthly_records_old_format():

    query = """
        SELECT 
            CASE 
                WHEN DAY(CURRENT_DATE) = 1 THEN 
                    SUBSTR(CAST(CURRENT_DATE - INTERVAL 1 MONTH AS CHAR), 1, 7)
                ELSE 
                    SUBSTR(CAST(CURRENT_DATE AS CHAR), 1, 7) 
            END AS MSTTLTL_SNAPSHOT_DATE,
            hrm.employee_id AS MSTTL_FSMID,
            (
                SELECT region.region_id 
                FROM RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND area.region_id = region.region_id
            ) AS MSTTL_REGID,
            fs.area_id AS MSTTL_MKTID,
            (
                SELECT region.region_name 
                FROM RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND area.region_id = region.region_id
            ) AS MSTTL_REGION,
            NULL AS MSTTL_OLD_REGION,
            NULL AS MSTTL_OLD_AREANAME,
            NULL AS MSTTL_AREANAME,
            (
                SELECT area.area_short_name 
                FROM RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id
            ) AS MSTTL_AREA,
            NULL AS MSTTL_BRANCH,
            (
                SELECT team.team_type_name 
                FROM RAC_FS_TM_TEAM_TYPE team 
                WHERE fs.team_type_id = team.team_type_id
            ) AS MSTTL_TEAM,
            NULL AS MSTTL_RBS_IKON,
            hr.resource_number AS MSTTL_TECHID,
            fs.employee_id AS MSTTL_EMP_NUM,
            hr.employee_name AS MSTTL_TECHNAME,
            (
                SELECT job.job_title 
                FROM RAC_FS_TM_JOB_CODE job 
                WHERE fs.job_id = job.job_id
            ) AS MSTTL_JOB_TITLE,
            (
                SELECT job.job_adp_code 
                FROM RAC_FS_TM_JOB_CODE job 
                WHERE fs.job_id = job.job_id
            ) AS MSTTL_JOB_TITLE_SHORTNAME,
            hr.email AS MSTTL_TECH_EMAIL,
            NULL AS MSTTL_TECH_CELL,
            NULL AS MSTTL_CELL_FORMAT,
            NULL AS MSTTL_ALTSURVEYCONTACT,
            NULL AS MSTTL_ALTSURVEYEMAIL,
            NULL AS MSTTL_TECH_PAGER,
            NULL AS MSTTL_TERRITORY_TYPE,
            hrm.employee_name AS MSTTL_FSM,
            hrm.email AS MSTTL_FSM_EMAIL,
            hrm.resource_number AS MSTTL_FSM_RESOURCE_NUMBER,
            hrm.employee_id AS MSTTL_FSM_EMPID,
            NULL AS MSTTL_TRAINING_ID,
            NULL AS MSTTL_UPDATE,
            NULL AS MSTTL_FTE,
            CASE
                WHEN fs.hr_status = 'Terminated' THEN 'Y'
                ELSE 'N' 
            END AS MSTTL_TERMED_Y_N,
            date_format(hr.actual_termination_date, '%d-%b-%Y') AS MSTTL_TERMED_DATE,
            date_format(hr.last_hire_date, '%d-%b-%Y') AS MSTTL_HIRE_DATE,
            NULL AS MSTTL_OTHER,
            NULL AS MSTTL_CHANGE,
            (
                SELECT employee_name 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND area.region_id = region.region_id 
                AND rdir.employee_id = region.region_dir_emp_id
            ) AS MSTTL_DISTRICT_DIR,
            (
                SELECT email 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND area.region_id = region.region_id 
                AND rdir.employee_id = region.region_dir_emp_id
            ) AS MSTTL_DISTRICT_DIR_EMAIL,
            (
                SELECT resource_number 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND area.region_id = region.region_id 
                AND rdir.employee_id = region.region_dir_emp_id
            ) AS MSTTL_DISTRICT_DIR_RESOURCE_NBR,
            (
                SELECT employee_id 
                FROM RAC_FS_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND area.region_id = region.region_id 
                AND rdir.employee_id = region.region_dir_emp_id
            ) AS MSTTL_DISTRICT_DIR_EMPLOYEEID,
            NULL AS MSTTL_DISTRICT_OPS,
            NULL AS MSTTL_DISTRICT_OPS_EMAIL,
            NULL AS MSTTL_DISTRICT_OPS_RESOURCE_NBR,
            NULL AS MSTTL_DISTRICT_OPS_EMPLOYEEID,
            (
                SELECT employee_name 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_dir_emp_id
            ) AS MSTTL_DIRECTOR,
            (
                SELECT email 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_dir_emp_id
            ) AS MSTTL_DIRECTOR_EMAIL,
            (
                SELECT resource_number 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_dir_emp_id
            ) AS MSTTL_DIRECTOR_RESOURCE_NBR,
            (
                SELECT employee_id 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_dir_emp_id
            ) AS MSTTL_DIRECTOR_EMPLOYEEID,
            (
                SELECT employee_name 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_fom_emp_id
            ) AS MSTTL_AREAOPS,
            (
                SELECT email 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_fom_emp_id
            ) AS MSTTL_AREAOPS_EMAIL,
            (
                SELECT RESOURCE_NUMBER 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_fom_emp_id
            ) AS MSTTL_AREAOPS_RESOURCE,
            (
                SELECT employee_id 
                FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area 
                WHERE area.area_id = fs.area_id 
                AND rdir.employee_id = area.area_fom_emp_id
            ) AS MSTTL_AREAOPS_EMPLOYEEID,
            NULL AS MSTTL_TECHADS,
            NULL AS MSTTL_LEAD_TECH_RESOURCE_NUMBER,
            NULL AS MSTTL_LEAD_TECH_RESOURCE_NAME,
            NULL AS MSTTL_LEAD_TECH_CELL_NUMBER,
            NULL AS MSTTL_PAGER_FORMAT,
            NULL AS MSTTL_EDGE,
            NULL AS MSTTL_PLATFORM,
            NULL AS MSTTL_BRANCHLOCATION,
            NULL AS MSTTL_JOB_CODE,
            (
                SELECT job.job_type 
                FROM RAC_FS_TM_JOB_CODE job 
                WHERE fs.job_id = job.job_id
            ) AS MSTTL_JOB_TYPE,
            fs.dedicated AS MSTTL_DROPSITE,
            NULL AS MSTTL_DROPSITEADD,
            NULL AS MSTTL_DROPSITECOUNTY,
            NULL AS MSTTL_SUBACCT,
            NULL AS MSTTL_R12_BRANCH_LOCATION,
            NULL AS MSTTL_TERRITORY_METHOD,
            NULL AS MSTTL_CSA_EMAIL,
            NULL AS MSTTL_CSA_DL_EMAIL,
            NULL AS MSTTL_EXCESS_CALL_LOAD,
            NULL AS MSTTL_CALL_LOAD_NOTIFICATION,
            hr.ebs_user_name AS MSTTL_IKON1_USERNAME,
            NULL AS MSTTL_DROPSITE2,
            NULL AS MSTTL_DROPSITEADD2,
            NULL AS MSTTL_DROPSITECOUNTY2,
            NULL AS MSTTL_SUBACCT2,
            NULL AS MSTTL_DROPSITE3,
            NULL AS MSTTL_DROPSITEADD3,
            NULL AS MSTTL_DROPSITECOUNTY3,
            NULL AS MSTTL_SUBACCT3,
            NULL AS MSTTL_TERRITORYMAKEUP,
            NULL AS MSTTL_ALLOWDRUMS,
            NULL AS MSTTL_ALLOWPCB,
            NULL AS MSTTL_ALLOWSUPPLIES,
            NULL AS MSTTL_LOCATION_CODE,
            NULL AS MSTTL_SALES_MARKETPLACE,
            NULL AS MSTTL_SALES_DISTRICT,
            fs.last_update_date AS MSTTL_UPDATED,
            NULL AS MSTTL_BUSINESS_TYPE
        FROM 
            RAC_FS_TM_EMPLOYEE_DTLS fs
        LEFT OUTER JOIN 
            RAC_HR_TM_EMPLOYEE_DTLS hr ON fs.employee_id = hr.employee_id
        LEFT OUTER JOIN 
            RAC_HR_TM_EMPLOYEE_DTLS hrm ON hrm.employee_id = fs.manager_id
    """
    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            connection.close()
            return records
        return records
    except Exception as e:
        print(str(e), "snowflake_old_records")
        logging.info(
            'Error snowflake_old_records from the database: %s', str(e))
        connection.close()
        return None


def snowflake_monthly_records_new_format():

    query = """
        SELECT
            CASE 
                WHEN DAY(CURRENT_DATE) = 1 THEN 
                    SUBSTR(CAST(CURRENT_DATE - INTERVAL 1 MONTH AS CHAR), 1, 7)
                ELSE 
                    SUBSTR(CAST(CURRENT_DATE AS CHAR), 1, 7) 
            END AS MSTTL_DATES,
            fs.employee_id AS MSTTL_EMPLOYEE_ID,
            hr.resource_number AS MSTTL_RESOURCE_NUMBER,
            fs.record_complete AS MSTTL_RECORD_COMPLETE,
            hr.contingent_Worker AS MSTTL_CONTINGENT_WORKER,
            hr.employee_name AS MSTTL_EMPLOYEE_NAME,
            hr.email AS MSTTL_EMPLOYEE_EMAIL,
            fs.alternate_email AS MSTTL_ADDITIONAL_EMPLOYEE_EMAIL,
            hr.ebs_user_name AS MSTTL_EBS_USER_NAME,
            fs.fs_status AS MSTTL_FS_STATUS,
            fs.business_org AS MSTTL_BUSINESS_ORG,
            (SELECT job.job_title FROM RAC_FS_TM_JOB_CODE job WHERE fs.job_id = job.job_id) AS MSTTL_JOB_TITLE,
            (SELECT job.job_type FROM RAC_FS_TM_JOB_CODE job WHERE fs.job_id = job.job_id) AS MSTTL_JOB_TYPE,
            fs.manager_flag AS MSTTL_MANAGER_FLAG,
            (SELECT job.job_adp_code FROM RAC_FS_TM_JOB_CODE job WHERE fs.job_id = job.job_id) AS MSTTL_JOB_ADP_CODE,
            CASE 
                WHEN (hr.JOB_TITLE != jc.JOB_TITLE OR hr.JOB_ADP != jc.JOB_ADP_CODE) THEN 'No'
                ELSE 'Yes' 
            END AS MSTTL_JOB_MATCH_TO_HR,
            (SELECT team.team_type_name FROM RAC_FS_TM_TEAM_TYPE team WHERE fs.team_type_id = team.team_type_id) AS MSTTL_TEAM_TYPE,
            fs.production_print AS MSTTL_OFSC_PRODUCTION_PRINT,
            region.REGION_NAME AS MSTTL_REGION,
            area.AREA_SHORT_NAME AS MSTTL_AREA_SHORT,
            hr.location_code AS MSTTL_LOCATION_CODE,
            CASE 
                WHEN (area_mgr.AREA_SHORT_NAME != area.AREA_SHORT_NAME OR region_mgr.REGION_NAME != region.REGION_NAME) THEN 'No'
                ELSE 'Yes' 
            END AS MSTTL_REGION_AND_AREA_MATCH_TO_HR,
            fs_mgr.employee_name AS MSTTL_MANAGER_NAME,
            fs_mgr.employee_id AS MSTTL_MANAGER_EMPLOYEE_ID,
            hrm.resource_number AS MSTTL_MANAGER_RESOURCE_NUM,
            hrm.email AS MSTTL_MANAGER_EMAIL,
            CASE 
                WHEN hr.MANAGER_EMPLOYEE_ID = fs.MANAGER_ID THEN 'Yes' 
                ELSE 'No' 
            END AS MSTTL_MANAGER_MATCH_TO_HR,
            fs.hr_status AS MSTTL_HR_STATUS,
            hr.last_hire_date AS MSTTL_LAST_HIRE_DATE,
            fs.service_start_date AS MSTTL_SERVICE_START_DATE,
            fs.service_end_date AS MSTTL_SERVICE_END_DATE,
            hr.actual_termination_date AS MSTTL_ACTUAL_TERMINATION_DATE,
            fs.absence_start_date AS MSTTL_ABSENCE_START_DATE,
            fs.absence_end_date AS MSTTL_ABSENCE_END_DATE,
            fs.actual_return_to_work AS MSTTL_ACTUAL_RETURN_TO_WORK,
            fs.work_shift AS MSTTL_WORK_SHIFT_1ST_2ND_3RD,
            fs.on_call AS MSTTL_ON_CALL,
            fs.on_site AS MSTTL_ON_SITE,
            fs.dedicated AS MSTTL_DEDICATED,
            fs.dedicated_to AS MSTTL_DEDICATED_TO,
            fs.service_advantage AS MSTTL_SERVICE_ADVANTAGE,
            (SELECT employee_name FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
            WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_NAME,
            (SELECT employee_id FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
            WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_EMPLOYEE_ID,
            (SELECT resource_number FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
            WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_RESOURCE_NUM,
            (SELECT email FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_REGION region, RAC_FS_TM_AREA area 
            WHERE area.area_id = fs.area_id AND area.region_id = region.region_id AND rdir.employee_id = region.region_dir_emp_id) AS MSTTL_REGION_DIR_EMAIL,
            (SELECT employee_name FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_NAME,
            (SELECT employee_id FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_EMPLOYEE_ID,
            (SELECT RESOURCE_NUMBER FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_RESOURCE_NUMBER,
            (SELECT email FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_dir_emp_id) AS MSTTL_AREA_DIR_EMAIL,
            (SELECT employee_name FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_NAME,
            (SELECT employee_id FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_EMPLOYEE_ID,
            (SELECT RESOURCE_NUMBER FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_RESOURCE_NUMBER,
            (SELECT email FROM RAC_HR_TM_EMPLOYEE_DTLS rdir, RAC_FS_TM_AREA area WHERE area.area_id = fs.area_id AND rdir.employee_id = area.area_fom_emp_id) AS MSTTL_AREA_FOM_EMAIL,
            (SELECT change_note FROM RAC_FS_TM_EMPLOYEE_UPD up WHERE up.employee_id = fs.employee_id AND up.change_status ='Processed' ORDER BY change_id DESC LIMIT 1) AS MSTTL_CHANGE_NOTE,
            (SELECT change_effective_date FROM RAC_FS_TM_EMPLOYEE_UPD up WHERE up.employee_id = fs.employee_id AND up.change_status ='Processed' ORDER BY change_id DESC LIMIT 1) AS MSTTL_CHANGE_EFFECTIVE_DATE,
            fs.admin_notes AS MSTTL_ADMIN_NOTES,
            fs.review_date AS MSTTL_REVIEW_DATE,
            NULL AS MSTTL_UPDATE_FLAG,
            fs.last_update_date AS MSTTL_LAST_UPDATE_DATE
        FROM 
            RAC_FS_TM_EMPLOYEE_DTLS fs
        LEFT OUTER JOIN 
            RAC_HR_TM_EMPLOYEE_DTLS hr ON fs.employee_id = hr.employee_id
        LEFT OUTER JOIN 
            RAC_HR_TM_EMPLOYEE_DTLS hrm ON hrm.employee_id = fs.manager_id
        LEFT OUTER JOIN 
            RAC_FS_TM_JOB_CODE jc ON jc.JOB_ID = fs.JOB_ID
        LEFT OUTER JOIN 
            RAC_FS_TM_EMPLOYEE_DTLS fs_mgr ON fs_mgr.employee_id = fs.manager_id
        LEFT OUTER JOIN 
            RAC_FS_TM_AREA AS area ON area.AREA_ID = fs.AREA_ID
        LEFT OUTER JOIN 
            RAC_FS_TM_REGION AS region ON region.REGION_ID = area.REGION_ID
        LEFT OUTER JOIN 
            RAC_FS_TM_AREA AS area_mgr ON area_mgr.AREA_ID = fs_mgr.AREA_ID
        LEFT OUTER JOIN 
            RAC_FS_TM_REGION AS region_mgr ON region_mgr.REGION_ID = area_mgr.REGION_ID
    """
    connection = DatabaseConnection().connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            connection.close()
            return records
        return records
    except Exception as e:
        print(str(e), "snowflake_new_records")
        logging.info(
            'Error snowflake_new_records from the database: %s', str(e))
        connection.close()
        return None


def snowflake_daily_data_upload_s3(**context):
    try:
        connection = DatabaseConnection().connect()
        records = snowflake_daily_records()

        if records:
            csv_file_path = create_snowflake_csv_from_daily_records(records)
            s3_bucket = TECH_MASTER_SNOWFLAKE_S3_BUCKET
            timestamp = datetime.utcnow().strftime('%m%d%Y')
            logger.info(f"timestamp : {timestamp}")
            file_name_format = f"Master_Techlist_Daily.csv"

            _s3_bucket = TECH_MASTER_S3_BUCKET
            _file_name_format = f"FAS_MASTER_TECHLIST_{timestamp}.csv"

            s3_key = f"{SF_S3_EXPORT_SNOWFLAKE_DAILY_KEY_PATH}/{file_name_format}"
            _s3_key = f"{TECH_MASTER_ENV}/{S3_EXPORT_SNOWFLAKE_DAILY_KEY_PATH}/{_file_name_format}"

            logger.info(f"s3_key : {s3_key}")
            upload_csv_to_s3(csv_file_path, s3_bucket, s3_key)
            upload_csv_to_s3(csv_file_path, _s3_bucket, _s3_key)

        else:
            logging.warning("No records found.")

    except Exception as e:
        logging.error("Error in snowflake records: %s", str(e))
    finally:
        if connection:
            connection.close()


def is_last_day_of_month():
    today = dt.now(local_tz)
    last_day = calendar.monthrange(today.year, today.month)[1]
    return today.day == last_day

def last_day_of_week():
    today = dt.now(local_tz)
    last_day_of_week = today + pendulum.duration(days=(calendar.FRIDAY - today.weekday() + 7) % 7)
    return last_day_of_week

def is_last_day_of_week():
    today = dt.now(local_tz)
    return today.weekday() == calendar.FRIDAY

def is_first_day_of_month():
    today = datetime.now(local_tz)
    return today.day == 1


def snowflake_monthly_data_upload_s3_old_format(**context):

    connection = None

    try:

        if not is_first_day_of_month():
            logging.info("Skipping job because it's not the first day of the month.")
            return True

        connection = DatabaseConnection().connect()
        records = snowflake_monthly_records_old_format()

        if records:
            csv_file_path = create_snowflake_csv_from_monthly_records_old_format(
                records)
            s3_bucket = TECH_MASTER_SNOWFLAKE_S3_BUCKET
            timestamp = datetime.utcnow().strftime('%m%d%Y')
            logger.info(f"timestamp : {timestamp}")
            file_name_format = f"Master_Techlist_Monthly_Old.csv"

            _s3_bucket = TECH_MASTER_S3_BUCKET
            _file_name_format = f"FAS_MASTER_TECHLIST_OLD_FORMAT_{timestamp}.csv"

            s3_key = f"{SF_S3_EXPORT_SNOWFLAKE_MONTHLY_OLD_FORMAT_KEY_PATH}/{file_name_format}"
            _s3_key = f"{TECH_MASTER_ENV}/{S3_EXPORT_SNOWFLAKE_MONTHLY_OLD_FORMAT_KEY_PATH}/{_file_name_format}"

            logger.info(f"s3_key : {s3_key}")
            upload_csv_to_s3(csv_file_path, s3_bucket, s3_key)
            upload_csv_to_s3(csv_file_path, _s3_bucket, _s3_key)

        else:
            logging.warning("No records found.")

    except Exception as e:
        logging.error("Error in snowflake old records: %s", str(e))
    finally:
        if connection:
            connection.close()


def snowflake_monthly_data_upload_s3_new_format(**context):

    connection = None

    try:

        if not is_first_day_of_month():
            logging.info("Skipping job because it's not the first day of the month.")
            return True

        connection = DatabaseConnection().connect()
        records = snowflake_monthly_records_new_format()

        if records:
            csv_file_path = create_snowflake_csv_from_monthly_records_new_format(
                records)
            s3_bucket = TECH_MASTER_SNOWFLAKE_S3_BUCKET
            timestamp = datetime.utcnow().strftime('%m%d%Y')
            logger.info(f"timestamp : {timestamp}")
            file_name_format = f"Master_Techlist_Monthly_New.csv"

            _s3_bucket = TECH_MASTER_S3_BUCKET
            _file_name_format = f"FAS_MASTER_TECHLIST_NEW_FORMAT_{timestamp}.csv"

            s3_key = f"{SF_S3_EXPORT_SNOWFLAKE_MONTHLY_NEW_FORMAT_KEY_PATH}/{file_name_format}"
            _s3_key = f"{TECH_MASTER_ENV}/{S3_EXPORT_SNOWFLAKE_MONTHLY_NEW_FORMAT_KEY_PATH}/{_file_name_format}"

            logger.info(f"s3_key : {s3_key}")
            upload_csv_to_s3(csv_file_path, s3_bucket, s3_key)
            upload_csv_to_s3(csv_file_path, _s3_bucket, _s3_key)

        else:
            logging.warning("No records found.")

    except Exception as e:
        logging.error("Error in snowflake new records: %s", str(e))
    finally:
        if connection:
            connection.close()

# Daily SnowFlake Job

def mt_RAW_PUB_DIM_FSA_MASTER_DAILY_TECHLIST(**context):

    try:
        service_url = "https://usw3.dm-us.informaticacloud.com/active-bpel/rt/tf_FSA_S3_RAPID_MASTER_TECHLIST_DAILY"

        job1 = requests.post(
            url=service_url,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                    'INFA-SESSION-ID': session.json()['icSessionId']}
        )
        finished = False
        while not finished:

            URL = '"https://usw3.dm-us.informaticacloud.com/active-bpel/services/tf/status/' + \
                job1.json()['RunId']
            status1 = requests.get(
                url=URL,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                        'INFA-SESSION-ID': session.json()['icSessionId']}
            )
            time.sleep(30)
            try:
                stat_val1 = status1.json()['status']
            except KeyError:
                stat_val1 = 'RUNNING'

            if (stat_val1 in ('SUCCESS', 'FAILED', 'SUSPENDED')):
                finished = True
                break
            else:
                finished = False

        logging.info(
            'mt_RAW_PUB_DIM_FSA_MASTER_DAILY_TECHLIST: %s', stat_val1)

        if (stat_val1 in ('FAILED', 'SUSPENDED')):
            logging.warning('Job Failed')
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.warning(f"Failed to execute mt_RAW_PUB_DIM_FSA_MASTER_DAILY_TECHLIST: {e}")

    return True


# Monthly SnowFlake Job

def mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_OLD_FORMAT_TECHLIST(**context):

    if not is_first_day_of_month():
        logging.info("Skipping job because it's not the first day of the month.")
        return True

    try:
        service_url = "https://usw3.dm-us.informaticacloud.com/active-bpel/rt/tf_FSA_S3_RAPID_MASTER_TECHLIST"
        
        job1 = requests.post(
            url=service_url,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                    'INFA-SESSION-ID': session.json()['icSessionId']}
        )
        logger.info("session %s", session.json())
        logger.info("job1 %s", job1.json())
        finished = False
        while not finished:

            URL = 'https://usw3.dm-us.informaticacloud.com/active-bpel/services/tf/status/' + \
                job1.json()['RunId']
            status1 = requests.get(
                url=URL,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                        'INFA-SESSION-ID': session.json()['icSessionId']}
            )
            time.sleep(30)
            try:
                stat_val1 = status1.json()['status']
            except KeyError:
                stat_val1 = 'RUNNING'

            if (stat_val1 in ('SUCCESS', 'FAILED', 'SUSPENDED')):
                finished = True
                break
            else:
                finished = False

        logging.info(
            'mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_OLD_FORMAT_TECHLIST: %s', stat_val1)

        if (stat_val1 in ('FAILED', 'SUSPENDED')):
            logging.warning('Job Failed')
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.warning(f"Failed to execute mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_OLD_FORMAT_TECHLIST: {e}")

    return True


def mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_OLD_FORMAT_SNAPSHOT(**context):

    if not is_first_day_of_month():
        logging.info("Skipping job because it's not the first day of the month.")
        return True

    try:
        service_url = "https://usw3.dm-us.informaticacloud.com/active-bpel/rt/tf_FSA_S3_RAPID_MASTER_TECHLIST_SNAPSHOT"

        job1 = requests.post(
            url=service_url,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                    'INFA-SESSION-ID': session.json()['icSessionId']}
        )
        finished = False
        while not finished:

            URL = 'https://usw3.dm-us.informaticacloud.com/active-bpel/services/tf/status/' + \
                job1.json()['RunId']
            status1 = requests.get(
                url=URL,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                        'INFA-SESSION-ID': session.json()['icSessionId']}
            )
            time.sleep(30)
            try:
                stat_val1 = status1.json()['status']
            except KeyError:
                stat_val1 = 'RUNNING'

            if (stat_val1 in ('SUCCESS', 'FAILED', 'SUSPENDED')):
                finished = True
                break
            else:
                finished = False

        logging.info(
            'mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_OLD_FORMAT_SNAPSHOT: %s', stat_val1)

        if (stat_val1 in ('FAILED', 'SUSPENDED')):
            logging.warning('Job Failed')
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.warning(f"Failed to execute mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_OLD_FORMAT_SNAPSHOT: {e}")

    return True


# New Format
def mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_NEW_FORMAT_TECHLIST(**context):

    if not is_first_day_of_month():
        logging.info("Skipping job because it's not the first day of the month.")
        return True

    try:
        service_url = "https://usw3.dm-us.informaticacloud.com/active-bpel/rt/tf_FSA_S3_RAPID_MASTER_TECHLIST_MONTHLY"

        job1 = requests.post(
            url=service_url,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                    'INFA-SESSION-ID': session.json()['icSessionId']}
        )
        logger.info("session %s", session.json())
        logger.info("job1 %s", job1.json())
        finished = False
        while not finished:

            URL = 'https://usw3.dm-us.informaticacloud.com/active-bpel/services/tf/status/' + \
                job1.json()['RunId']
            status1 = requests.get(
                url=URL,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                        'INFA-SESSION-ID': session.json()['icSessionId']}
            )
            time.sleep(30)
            try:
                stat_val1 = status1.json()['status']
            except KeyError:
                stat_val1 = 'RUNNING'

            if (stat_val1 in ('SUCCESS', 'FAILED', 'SUSPENDED')):
                finished = True
                break
            else:
                finished = False

        logging.info(
            'mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_NEW_FORMAT_TECHLIST: %s', stat_val1)

        if (stat_val1 in ('FAILED', 'SUSPENDED')):
            logging.warning('Job Failed')
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.warning(f"Failed to execute mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_NEW_FORMAT_TECHLIST: {e}")

    return True


def mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_NEW_FORMAT_SNAPSHOT(**context):

    if not is_first_day_of_month():
        logging.info("Skipping job because it's not the first day of the month.")
        return True

    try:
        service_url = "https://usw3.dm-us.informaticacloud.com/active-bpel/rt/tf_FSA_S3_RAPID_MASTER_TECHLIST_SNAPSHOT_MONTHLY"

        job1 = requests.post(
            url=service_url,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                    'INFA-SESSION-ID': session.json()['icSessionId']}
        )
        finished = False
        while not finished:

            URL = 'https://usw3.dm-us.informaticacloud.com/active-bpel/services/tf/status/' + \
                job1.json()['RunId']
            status1 = requests.get(
                url=URL,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                        'INFA-SESSION-ID': session.json()['icSessionId']}
            )
            time.sleep(30)
            try:
                stat_val1 = status1.json()['status']
            except KeyError:
                stat_val1 = 'RUNNING'

            if (stat_val1 in ('SUCCESS', 'FAILED', 'SUSPENDED')):
                finished = True
                break
            else:
                finished = False

        logging.info(
            'mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_NEW_FORMAT_SNAPSHOT: %s', stat_val1)

        if (stat_val1 in ('FAILED', 'SUSPENDED')):
            logging.warning('Job Failed')
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.warning(f"Failed to execute mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_NEW_FORMAT_SNAPSHOT: {e}")

    return True


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

# SnowFlake daily basis Dag's

RAC_SNOWFLAKE_DAILY_DATA_UPLOAD_S3 = PythonOperator(
    task_id='RAC_SNOWFLAKE_DAILY_DATA_UPLOAD_S3',
    python_callable=snowflake_daily_data_upload_s3,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_mt_RAW_PUB_DIM_FSA_MASTER_DAILY_TECHLIST = PythonOperator(
    task_id='RAC_mt_RAW_PUB_DIM_FSA_MASTER_DAILY_TECHLIST',
    python_callable=mt_RAW_PUB_DIM_FSA_MASTER_DAILY_TECHLIST,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

# SnowFlake monthly basis Dag's old format

RAC_SNOWFLAKE_MONTHLY_DATA_UPLOAD_S3_OLD_FORMAT = PythonOperator(
    task_id='RAC_SNOWFLAKE_MONTHLY_DATA_UPLOAD_S3_OLD_FORMAT',
    python_callable=snowflake_monthly_data_upload_s3_old_format,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_OLD_FORMAT_TECHLIST = PythonOperator(
    task_id='RAC_mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_OLD_FORMAT_TECHLIST',
    python_callable=mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_OLD_FORMAT_TECHLIST,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_OLD_FORMAT_SNAPSHOT = PythonOperator(
    task_id='RAC_mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_OLD_FORMAT_SNAPSHOT',
    python_callable=mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_OLD_FORMAT_SNAPSHOT,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

# SnowFlake monthly basis Dag's new format

RAC_SNOWFLAKE_MONTHLY_DATA_UPLOAD_S3_NEW_FORMAT = PythonOperator(
    task_id='RAC_SNOWFLAKE_MONTHLY_DATA_UPLOAD_S3_NEW_FORMAT',
    python_callable=snowflake_monthly_data_upload_s3_new_format,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_NEW_FORMAT_TECHLIST = PythonOperator(
    task_id='RAC_mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_NEW_FORMAT_TECHLIST',
    python_callable=mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_NEW_FORMAT_TECHLIST,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_NEW_FORMAT_SNAPSHOT = PythonOperator(
    task_id='RAC_mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_NEW_FORMAT_SNAPSHOT',
    python_callable=mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_NEW_FORMAT_SNAPSHOT,
    email_on_failure=True,
    email_on_success=True,
    provide_context=True,
    dag=dag
)

RAC_SNOWFLAKE_DAILY_DATA_UPLOAD_S3 \
    >> RAC_SNOWFLAKE_MONTHLY_DATA_UPLOAD_S3_OLD_FORMAT \
    >> RAC_SNOWFLAKE_MONTHLY_DATA_UPLOAD_S3_NEW_FORMAT \
    >> RAC_mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_OLD_FORMAT_TECHLIST \
    >> RAC_mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_OLD_FORMAT_SNAPSHOT \
    >> RAC_mt_RAW_PUB_DIM_FSA_MASTER_MONTHLY_NEW_FORMAT_TECHLIST \
    >> RAC_mt_PUB_DIM_FSA_MASTER_TECHLIST_MONTHLY_NEW_FORMAT_SNAPSHOT \
    >> RAC_mt_RAW_PUB_DIM_FSA_MASTER_DAILY_TECHLIST \
    >> t2
