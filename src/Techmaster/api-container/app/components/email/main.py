import os
import smtplib
from email.message import EmailMessage


def send_email_csa(recipient_email, old_data, new_data):
    try:
        print("in email")
        smtp_server = os.environ.get("SMTP_SERVER")
        from_address = os.environ.get("FROM_ADDRESS")

        if not smtp_server or not from_address:
            raise ValueError("SMTP_SERVER or FROM_ADDRESS are not set.")

        employee_name = (
            new_data.get("EMPLOYEE_NAME")
            if new_data.get("EMPLOYEE_NAME") is not None
            else ""
        )
        area = new_data.get("AREA") if new_data.get("AREA") is not None else ""

        subject = "Techmaster Change for Employee: " + employee_name + ". Area: " + area
        body = """<style> table td, table tr {
                border: 1px solid #AAAAAA;
                padding: 3px;
                }
                </style>"""
        body += f"<br>The following changes have been applied to the Tech Master Database<br>"
        body += f"<table>"
        body += f"<tr><td>CSA Change Comment Log</td><td></td><td>{new_data['CSA_CHANGE_COMMENT']}</td></tr>"
        body += f"<tr><td>Last Edited Date</td><td></td><td>{new_data['LAST_UPDATE_DATE']}</td></tr>"
        body += f"<tr><td>Last Edited By</td><td></td><td>{new_data['LAST_UPDATED_BY']}</td></tr>"
        body += f"<tr><td>Creation Date</td><td>{old_data['CREATION_DATE']}</td><td>{new_data['CREATION_DATE']}</td></tr>"
        body += (
            f"<tr><td>Change Type</td><td></td><td>{new_data['CHANGE_TYPE']}</td></tr>"
        )
        body += f"<tr><td>Employee ID</td><td>{old_data['EMPLOYEE_ID']}</td><td>{new_data['EMPLOYEE_ID']}</td></tr>"
        # body+=f"<tr><td>Business Org</td><td>{old_data['']}</td><td>{new_data['']}</td></tr>"
        body += f"<tr><td>Resource Number</td><td>{old_data['RESOURCE_NUMBER']}</td><td>{new_data['RESOURCE_NUMBER']}</td></tr>"
        body += f"<tr><td>Employee Name</td><td>{old_data['EMPLOYEE_NAME']}</td><td>{new_data['EMPLOYEE_NAME']}</td></tr>"
        body += f"<tr><td>Email Address</td><td>{old_data['EMAIL']}</td><td>{new_data['EMAIL']}</td></tr>"
        body += f"<tr><td>FS Status</td><td>{old_data['FS_STATUS']}</td><td>{new_data['FS_STATUS']}</td></tr>"
        body += f"<tr><td>Absence Start Date</td><td>{old_data['ABSENCE_START_DATE']}</td><td>{new_data['ABSENCE_START_DATE']}</td></tr>"
        body += f"<tr><td>Absence End Date</td><td>{old_data['ABSENCE_END_DATE']}</td><td>{new_data['ABSENCE_END_DATE']}</td></tr>"
        body += f"<tr><td>Region</td><td>{old_data['REGION']}</td><td>{new_data['REGION']}</td></tr>"
        body += f"<tr><td>Area</td><td>{old_data['AREA']}</td><td>{new_data['AREA']}</td></tr>"
        body += f"<tr><td>Location Code</td><td>{old_data['LOC_CODE']}</td><td>{new_data['LOC_CODE']}</td></tr>"
        body += f"<tr><td>Manager Resource Number</td><td>{old_data['MANAGER_RESOURCE_NUMBER']}</td><td>{new_data['MANAGER_RESOURCE_NUMBER']}</td></tr>"
        body += f"<tr><td>Manager Name</td><td>{old_data['MANAGER_NAME']}</td><td>{new_data['MANAGER_NAME']}</td></tr>"
        body += f"<tr><td>Manager Email</td><td>{old_data['MANAGER_EMAIL']}</td><td>{new_data['MANAGER_EMAIL']}</td></tr>"
        body += f"<tr><td>Area Dir Name</td><td>{old_data['AREA_DIR_NAME']}</td><td>{new_data['AREA_DIR_NAME']}</td></tr>"
        body += f"<tr><td>Area Dir Email</td><td>{old_data['AREA_DIR_EMAIL']}</td><td>{new_data['AREA_DIR_EMAIL']}</td></tr>"
        body += f"<tr><td>Team Type</td><td>{old_data['TEAM_TYPE']}</td><td>{new_data['TEAM_TYPE']}</td></tr>"
        body += f"<tr><td>Additional Email</td><td>{old_data['ALTERNATE_EMAIL']}</td><td>{new_data['ALTERNATE_EMAIL']}</td></tr>"
        body += f"<tr><td>Job Title</td><td>{old_data['JOB_TITLE']}</td><td>{new_data['JOB_TITLE']}</td></tr>"
        body += f"<tr><td>Actual Termination Date</td><td>{old_data['ACTUAL_TERMINATION_DATE']}</td><td>{new_data['ACTUAL_TERMINATION_DATE']}</td></tr>"
        body += f"<tr><td>Approved By</td><td>{old_data['APPROVED_BY']}</td><td>{new_data['APPROVED_BY']}</td></tr>"
        body += f"<tr><td>Change Note</td><td>{old_data['CHANGE_NOTE']}</td><td>{new_data['CHANGE_NOTE']}</td></tr>"
        body += f"<tr><td>HR Status</td><td>{old_data['HR_STATUS']}</td><td>{new_data['HR_STATUS']}</td></tr>"
        body += f"<tr><td>Requested By</td><td>{old_data['REQUESTED_BY']}</td><td>{new_data['REQUESTED_BY'].strip()}</td></tr>"
        # body+=f"<tr><td>Absence Start Date</td><td>{old_data['']}</td><td>{new_data['']}</td></tr>"
        # body+=f"<tr><td>Absence End Date</td><td>{old_data['']}</td><td>{new_data['']}</td></tr>"
        # body+=f"<tr><td>Actual Return to Work</td><td>{old_data['']}</td><td>{new_data['']}</td></tr>"
        body += f"</table>"
        body += f"<br>NOTE : This is a system generated email,***No reply required***<br><br>Thank you"

        print(body)
        print(recipient_email)
        msg = EmailMessage()
        msg.set_content(body)
        msg.add_alternative(body, subtype="html")
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = recipient_email
        smtp_client = smtplib.SMTP(smtp_server)
        smtp_client.sendmail(from_address, recipient_email, msg.as_string())
        smtp_client.quit()
        # print(smtp_client)

        return "Email Sent"

    except Exception as e:
        print(e)
        return "Email Error"
