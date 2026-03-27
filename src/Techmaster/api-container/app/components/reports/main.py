import json
from datetime import date as dates, timedelta

from flask import Blueprint, request
from sqlalchemy import desc, or_, text, func
from sqlalchemy.orm import aliased
from collections import OrderedDict

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

report_router = Blueprint("report", __name__)


# This endpoint will be used for the report filter section.
# It can be used in the ALL  records.
@report_router.route("/get_all_active_list", methods=["GET"])
@requestValidation.validate
def get_all_active_list():
    try:
        # Extract query parameters from the request
        types = request.args.get("type")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION)
            tab_hrm_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)

            # Build the query to fetch data
            query = session.query(
                tab_fs_emp.EMPLOYEE_ID,
                tab_hr_tm.EMPLOYEE_NAME,
                tab_hr_tm.RESOURCE_NUMBER,
                tab_hrm_tm.EMPLOYEE_NAME.label("MANAGER_NAME"),
                tab_fs_emp.MANAGER_ID,
                tab_hr_tm.EMAIL,
                tab_hr_tm.AREA,
                tab_reg.REGION_NAME,
                tab_area.AREA_SHORT_NAME,
                tab_team.TEAM_TYPE_NAME,
                tab_job.JOB_TITLE,
                #tab_job.JOB_CODE,
                tab_job.JOB_ADP_CODE,
                tab_fs_emp.LOCATION_CODE,
                tab_fs_emp.MANAGER_FLAG,
                tab_fs_emp.WORK_SHIFT,
                tab_fs_emp.ON_CALL,
                tab_fs_emp.ON_SITE,
                tab_fs_emp.DEDICATED,
                tab_fs_emp.DEDICATED_TO,
                tab_fs_emp.SERVICE_ADVANTAGE,
                tab_fs_emp.FS_STATUS,
                tab_fs_emp.SERVICE_START_DATE,
                tab_fs_emp.SERVICE_END_DATE,
                tab_fs_emp.RECORD_COMPLETE,
                tab_hr_tm.LAST_HIRE_DATE,
                tab_hr_tm.ACTUAL_TERMINATION_DATE,
                tab_hr_tm.ABSENCE_START_DATE,
                tab_hr_tm.ABSENCE_END_DATE
            ).join(
                tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID
            ).outerjoin(
                tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID
            ).outerjoin(
                tab_area, tab_area.AREA_ID == tab_fs_emp.AREA_ID
            ).outerjoin(
                tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID
            ).outerjoin(
                tab_hrm_tm, tab_hrm_tm.EMPLOYEE_ID == tab_fs_emp.MANAGER_ID
            ).outerjoin(
                tab_job, tab_job.JOB_ID == tab_fs_emp.JOB_ID
            )
            if types.upper() == 'ALL':
                total_items = query.count()
                results = query.all()
            elif types.upper() == 'ACTIVE':
                query = query.filter(
                    or_(
                        tab_hr_tm.ACTUAL_TERMINATION_DATE.is_(None),
                        tab_hr_tm.ACTUAL_TERMINATION_DATE > text("utc_date()"),
                        tab_hr_tm.ACTUAL_TERMINATION_DATE == "",
                    )
                )
                total_items = query.count()
                results = query.all()
            else:
                error_response = [
                    {"status": "Success", "message": "Please select Employee"}
                ]
                return (
                    json.loads(APIResponse(errors=error_response).to_json()),
                    400,
                )
            response_data = {
                "records": [
                    {
                        "Employee Id": result.EMPLOYEE_ID,
                        "Employee Name": result.EMPLOYEE_NAME,
                        "Resource Number": result.RESOURCE_NUMBER,
                        "Email": result.EMAIL,
                        "Manager Id": result.MANAGER_ID,
                        "Manager Name": result.MANAGER_NAME,
                        "Team Type Name": result.TEAM_TYPE_NAME,
                        #"Area Name": result.AREA,
                        "Area Short Name": result.AREA_SHORT_NAME,
                        "Region Name": result.REGION_NAME,
                        "Job Title": result.JOB_TITLE,
                        #"Job Code": result.JOB_CODE,
                        "Job Adp Code": result.JOB_ADP_CODE,
                        "Location Code": result.LOCATION_CODE,
                        "Manager Flag": result.MANAGER_FLAG,
                        "Work Shift": result.WORK_SHIFT,
                        "On Call": result.ON_CALL,
                        "On Site": result.ON_SITE,
                        "Dedicated": result.DEDICATED,
                        "Dedicated To": result.DEDICATED,
                        "Service Advantage": result.SERVICE_ADVANTAGE,
                        "Fs Status": result.FS_STATUS,
                        "Service Start Date": dates.strftime(
                            result.SERVICE_START_DATE, "%m-%d-%Y") if result.SERVICE_START_DATE else None,
                        "Service End Date": dates.strftime(
                            result.SERVICE_END_DATE, "%m-%d-%Y") if result.SERVICE_END_DATE else None,
                        "Record Complete": result.RECORD_COMPLETE,
                        "Last Hire Date": dates.strftime(
                            result.LAST_HIRE_DATE, "%m-%d-%Y") if result.LAST_HIRE_DATE else None,
                        "Actual Termination Date": dates.strftime(
                            result.ACTUAL_TERMINATION_DATE, "%m-%d-%Y") if result.ACTUAL_TERMINATION_DATE else None,
                        "Absence Start Date": dates.strftime(
                            result.ABSENCE_START_DATE, "%m-%d-%Y") if result.ABSENCE_START_DATE else None,
                        "Absence End Date": dates.strftime(
                            result.ABSENCE_END_DATE, "%m-%d-%Y") if result.ABSENCE_END_DATE else None
                    }
                    for result in results
                ],
                "status": "Success",
                "message": "Data retrieved successfully",
                "total_items": total_items,
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500