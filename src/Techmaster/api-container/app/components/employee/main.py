import json
from datetime import date as dates
from datetime import datetime
from datetime import datetime as dt

from flask import Blueprint, request
from sqlalchemy import desc, func, or_, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_employee_update import (
    racFsTmEmployeeUpdateCreate,
    racFsTmEmployeeUpdateHierarchy,
    racFsTmEmployeeUpdateJob,
    racFsTmEmployeeUpdateManager,
    racFsTmEmployeeUpdateSchema,
)
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse
from app.lib.core.services.base_service import baseService

employee_router = Blueprint("employee", __name__)


# This endpoint used for view employee screen
# Data's will fetched based on {employee_id}
@employee_router.route("/get", methods=["GET"])
@requestValidation.validate
def fetch_employee_info():
    try:
        employee_id = request.args.get("employee_id")
        if not employee_id:
            error_response = [
                {"status": "Failed", "message": "employee_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="tab_fs_emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="tab_hr_tm"
            )
            # Build the query to fetch manager data
            employee_Info_query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_fs_emp.MANAGER_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.AREA_ID,
                    tab_fs_emp.LOCATION_CODE,
                    tab_fs_emp.JOB_ID,
                    tab_fs_emp.TEAM_TYPE_ID,
                    tab_fs_emp.CIP,
                    tab_fs_emp.WORK_SHIFT,
                    tab_fs_emp.ON_CALL,
                    tab_fs_emp.ON_SITE,
                    tab_fs_emp.DEDICATED,
                    tab_fs_emp.DEDICATED_TO,
                    tab_fs_emp.SERVICE_ADVANTAGE,
                    tab_fs_emp.FS_STATUS,
                    tab_fs_emp.PRODUCTION_PRINT,
                    tab_fs_emp.SERVICE_START_DATE,
                    tab_fs_emp.SERVICE_END_DATE,
                    tab_fs_emp.RECORD_COMPLETE,
                    tab_fs_emp.MANAGER_FLAG,
                    tab_fs_emp.ALTERNATE_EMAIL,
                    tab_fs_emp.BUSINESS_ORG.label("BUSINESS_ORG"),
                    tab_hr_tm.MANAGER_NAME.label("HR_MANAGER_NAME"),
                    tab_hr_tm.MANAGER_EMPLOYEE_ID.label("HR_MANAGER_EMPLOYEE_ID"),
                    tab_hr_tm.EMPLOYEE_NAME.label("HR_EMPLOYEE_NAME"),
                    tab_hr_tm.EMAIL.label("HR_EMAIL"),
                    tab_hr_tm.RESOURCE_NUMBER.label("HR_RESOURCE_NUMBER"),
                    tab_hr_tm.REGION.label("HR_REGION"),
                    tab_hr_tm.AREA.label("HR_AREA"),
                    tab_hr_tm.AREA_SHORT.label("HR_AREA_SHORT"),
                    tab_hr_tm.LOCATION_CODE.label("HR_LOCATION_CODE"),
                    tab_hr_tm.JOB_TITLE.label("HR_JOB_TITLE"),
                    tab_hr_tm.JOB_CODE.label("HR_JOB_CODE"),
                    tab_hr_tm.JOB_ADP.label("HR_JOB_ADP"),
                    tab_hr_tm.CONTINGENT_WORKER.label("HR_CONTINGENT_WORKER"),
                    tab_hr_tm.ACTUAL_TERMINATION_DATE.label(
                        "HR_ACTUAL_TERMINATION_DATE"
                    ),
                    tab_fs_emp.ABSENCE_START_DATE.label("HR_ABSENCE_START_DATE"),
                    tab_fs_emp.ABSENCE_END_DATE.label("HR_ABSENCE_END_DATE"),
                    tab_fs_emp.ACTUAL_RETURN_TO_WORK.label("HR_ACTUAL_RETURN_TO_WORK"),
                    tab_hr_tm.ORG_CODE.label("HR_ORG_CODE"),
                    tab_hr_tm.LAST_HIRE_DATE.label("HR_LAST_HIRE_DATE"),
                    tab_hr_tm.EBS_USER_NAME.label("HR_EBS_USER_NAME"),
                    tab_hr_tm.LAST_UPDATE_DATE.label("LAST_UPDATE_DATE"),
                    func.RAC_FS_TM_GET_USER_NAME(tab_hr_tm.LAST_UPDATED_BY).label(
                        "LAST_UPDATED_BY"
                    ),
                    tab_fs_emp.HR_STATUS.label("HR_STATUS"),
                    tab_fs_emp.REVIEW_DATE,
                )
                .outerjoin(tab_fs_emp, tab_hr_tm.EMPLOYEE_ID == tab_fs_emp.EMPLOYEE_ID)
                .filter(tab_hr_tm.EMPLOYEE_ID == employee_id)
                .first()
            )

            if employee_Info_query:
                employee_section = {
                    "employee_id": employee_Info_query.EMPLOYEE_ID,
                    "employee_name": employee_Info_query.HR_EMPLOYEE_NAME,
                    "email": employee_Info_query.HR_EMAIL,
                    "resource_number": employee_Info_query.HR_RESOURCE_NUMBER,
                    "admin_notes": employee_Info_query.ADMIN_NOTES,
                    "alternate_email": employee_Info_query.ALTERNATE_EMAIL,
                }

                tab_area_m = aliased(
                    initialize.db_tables.RAC_FS_TM_AREA, name="tab_area_m"
                )
                tab_region_m = aliased(
                    initialize.db_tables.RAC_FS_TM_REGION, name="tab_region_m"
                )
                tab_fs_emp_m = aliased(
                    initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="tab_fs_emp_m"
                )
                # tab_location = aliased(initialize.db_tables.RAC_FS_TM_LOC)

                manager_hierarchy_query = (
                    session.query(
                        tab_fs_emp_m.EMPLOYEE_ID,
                        tab_area_m.AREA_SHORT_NAME,
                        tab_region_m.REGION_NAME,
                        tab_area_m.STATUS.label("AREA_STATUS"),
                        tab_region_m.STATUS.label("REGION_STATUS"),
                    )
                    .filter(tab_fs_emp_m.EMPLOYEE_ID == employee_Info_query.MANAGER_ID)
                    .join(tab_area_m, tab_fs_emp_m.AREA_ID == tab_area_m.AREA_ID)
                    .join(tab_region_m, tab_region_m.REGION_ID == tab_area_m.REGION_ID)
                    .first()
                )

                tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="tab_area")
                tab_region = aliased(
                    initialize.db_tables.RAC_FS_TM_REGION, name="tab_region"
                )
                configuration_Info_query = (
                    session.query(
                        tab_area.AREA_SHORT_NAME,
                        tab_region.REGION_NAME,
                        tab_area.STATUS.label("AREA_STATUS"),
                        tab_region.STATUS.label("REGION_STATUS"),
                    )
                    .join(tab_region, tab_region.REGION_ID == tab_area.REGION_ID)
                    .filter(tab_area.AREA_ID == employee_Info_query.AREA_ID)
                    .first()
                )
                if configuration_Info_query and manager_hierarchy_query:
                    location_match_to_hr = "Yes"
                    if (
                        # employee_Info_query.LOCATION_CODE
                        # != employee_Info_query.HR_LOCATION_CODE
                        # or
                        configuration_Info_query.AREA_SHORT_NAME
                        != manager_hierarchy_query.AREA_SHORT_NAME
                        or configuration_Info_query.REGION_NAME
                        != manager_hierarchy_query.REGION_NAME
                    ):
                        location_match_to_hr = "No"
                else:
                    location_match_to_hr = "No"

                if employee_Info_query.EMPLOYEE_ID != None:
                    hierarchy_section = {
                        "location_code": employee_Info_query.LOCATION_CODE,
                        "area_short_name": configuration_Info_query.AREA_SHORT_NAME
                        if configuration_Info_query
                        else None,
                        "region_name": configuration_Info_query.REGION_NAME
                        if configuration_Info_query
                        else None,
                        "location_match_to_hr": location_match_to_hr
                        if configuration_Info_query
                        else "No",
                        "region_status": configuration_Info_query.REGION_STATUS
                        if configuration_Info_query
                        else None,
                        "area_status": configuration_Info_query.AREA_STATUS
                        if configuration_Info_query
                        else None,
                        "system": {
                            "system_region_name": manager_hierarchy_query.REGION_NAME
                            if manager_hierarchy_query
                            else None,
                            "system_area_name": manager_hierarchy_query.AREA_SHORT_NAME
                            if manager_hierarchy_query
                            else None,
                            "system_area_short_name": manager_hierarchy_query.AREA_SHORT_NAME
                            if manager_hierarchy_query
                            else None,
                            "system_location_code": None,
                        },
                    }

                else:
                    # Populate hierarchy_section for new hire
                    manager_hierarchy_query_hr = (
                        session.query(
                            tab_fs_emp_m.EMPLOYEE_ID,
                            tab_area_m.AREA_SHORT_NAME,
                            tab_region_m.REGION_NAME,
                            tab_area_m.STATUS.label("AREA_STATUS"),
                            tab_region_m.STATUS.label("REGION_STATUS"),
                        )
                        .filter(
                            tab_fs_emp_m.EMPLOYEE_ID
                            == employee_Info_query.HR_MANAGER_EMPLOYEE_ID
                        )
                        .join(tab_area_m, tab_fs_emp_m.AREA_ID == tab_area_m.AREA_ID)
                        .join(
                            tab_region_m, tab_region_m.REGION_ID == tab_area_m.REGION_ID
                        )
                        .first()
                    )
                    hierarchy_section = {
                        "location_code": None,
                        "area_short_name": configuration_Info_query.AREA_SHORT_NAME
                        if configuration_Info_query
                        else None,
                        "region_name": configuration_Info_query.REGION_NAME
                        if configuration_Info_query
                        else None,
                        "location_match_to_hr": "Yes",
                        "region_status": configuration_Info_query.REGION_STATUS
                        if configuration_Info_query
                        else None,
                        "area_status": configuration_Info_query.AREA_STATUS
                        if configuration_Info_query
                        else None,
                        "system": {
                            "system_region_name": manager_hierarchy_query_hr.REGION_NAME
                            if manager_hierarchy_query_hr
                            else None,
                            "system_area_name": manager_hierarchy_query_hr.AREA_SHORT_NAME
                            if manager_hierarchy_query_hr
                            else None,
                            "system_area_short_name": manager_hierarchy_query_hr.AREA_SHORT_NAME
                            if manager_hierarchy_query_hr
                            else None,
                            "system_location_code": None,
                        },
                    }

                tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)

                job_Info_query = (
                    session.query(
                        tab_job_code.JOB_ID,
                        tab_job_code.JOB_TITLE,
                        tab_job_code.JOB_TYPE,
                        tab_job_code.JOB_ADP_CODE,
                        tab_job_code.STATUS,
                    )
                    .filter(tab_job_code.JOB_ID == employee_Info_query.JOB_ID)
                    .first()
                )
                job_match_to_hr = "Yes"
                if job_Info_query:
                    if (
                        # job_Info_query.JOB_TITLE != employee_Info_query.HR_JOB_TITLE
                        # or
                        job_Info_query.JOB_ADP_CODE
                        != employee_Info_query.HR_JOB_ADP
                    ):
                        job_match_to_hr = "No"

                # Populates Employee Job section
                employee_job_code_section = {
                    "job_id": job_Info_query.JOB_ID if job_Info_query else None,
                    "job_title": job_Info_query.JOB_TITLE if job_Info_query else None,
                    "job_type": job_Info_query.JOB_TYPE if job_Info_query else None,
                    "job_adp_code": job_Info_query.JOB_ADP_CODE
                    if job_Info_query
                    else None,
                    "job_match_to_hr": job_match_to_hr,
                    "job_status": job_Info_query.STATUS if job_Info_query else None,
                    "system": {
                        "system_job_title": employee_Info_query.HR_JOB_TITLE,
                        "system_job_code": employee_Info_query.HR_JOB_CODE,
                        "system_job_adp_code": employee_Info_query.HR_JOB_ADP,
                    },
                }

                tab_team_type = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)

                team_type_Info_query = (
                    session.query(
                        tab_team_type.TEAM_TYPE_ID,
                        tab_team_type.TEAM_TYPE_NAME,
                        tab_team_type.STATUS,
                    )
                    .filter(
                        tab_team_type.TEAM_TYPE_ID == employee_Info_query.TEAM_TYPE_ID
                    )
                    .first()
                )

                # Populates Service Section
                service_section = {
                    "business_org": employee_Info_query.BUSINESS_ORG
                    if employee_Info_query.BUSINESS_ORG
                    else None,
                    "job_type": job_Info_query.JOB_TYPE if job_Info_query else None,
                    "team_type": team_type_Info_query.TEAM_TYPE_NAME
                    if employee_Info_query.TEAM_TYPE_ID
                    else None,
                    "team_status": team_type_Info_query.STATUS
                    if employee_Info_query.TEAM_TYPE_ID
                    else None,
                    "cip": employee_Info_query.CIP if employee_Info_query.CIP else None,
                    "work_shift": employee_Info_query.WORK_SHIFT
                    if employee_Info_query.WORK_SHIFT
                    else None,
                    "on_call": employee_Info_query.ON_CALL
                    if employee_Info_query.ON_CALL
                    else None,
                    "on_site": employee_Info_query.ON_SITE
                    if employee_Info_query.ON_SITE
                    else None,
                    "dedicated": employee_Info_query.DEDICATED
                    if employee_Info_query.DEDICATED
                    else None,
                    "dedicated_to": employee_Info_query.DEDICATED_TO
                    if employee_Info_query.DEDICATED_TO
                    else None,
                    "service_advantage": employee_Info_query.SERVICE_ADVANTAGE
                    if employee_Info_query.SERVICE_ADVANTAGE
                    else None,
                    "contingent_worker": employee_Info_query.HR_CONTINGENT_WORKER
                    if employee_Info_query.HR_CONTINGENT_WORKER
                    else None,
                    "fs_status": employee_Info_query.FS_STATUS
                    if employee_Info_query.FS_STATUS
                    else None,
                    "production_print": employee_Info_query.PRODUCTION_PRINT
                    if employee_Info_query.PRODUCTION_PRINT
                    else None,
                    "service_start_date": dates.strftime(
                        employee_Info_query.SERVICE_START_DATE, "%m-%d-%Y"
                    )
                    if employee_Info_query.SERVICE_START_DATE
                    else None,
                    "service_end_date": dates.strftime(
                        employee_Info_query.SERVICE_END_DATE, "%m-%d-%Y"
                    )
                    if employee_Info_query.SERVICE_END_DATE
                    else None,
                    "record_complete": employee_Info_query.RECORD_COMPLETE
                    if employee_Info_query.RECORD_COMPLETE
                    else None,
                }

                # Populates HR Status Section
                hr_status_section = {
                    "actual_termination_date": dates.strftime(
                        employee_Info_query.HR_ACTUAL_TERMINATION_DATE,
                        "%m-%d-%Y",
                    )
                    if employee_Info_query.HR_ACTUAL_TERMINATION_DATE
                    else None,
                    "absence_start_date": dates.strftime(
                        employee_Info_query.HR_ABSENCE_START_DATE, "%m-%d-%Y"
                    )
                    if employee_Info_query.HR_ABSENCE_START_DATE
                    else None,
                    "absence_end_date": dates.strftime(
                        employee_Info_query.HR_ABSENCE_END_DATE, "%m-%d-%Y"
                    )
                    if employee_Info_query.HR_ABSENCE_END_DATE
                    else None,
                    "actual_return_to_work": dates.strftime(
                        employee_Info_query.HR_ACTUAL_RETURN_TO_WORK,
                        "%m-%d-%Y",
                    )
                    if employee_Info_query.HR_ACTUAL_RETURN_TO_WORK
                    else None,
                    "last_hire_date": dates.strftime(
                        employee_Info_query.HR_LAST_HIRE_DATE, "%m-%d-%Y"
                    )
                    if employee_Info_query.HR_LAST_HIRE_DATE
                    else None,
                    "hr_status": employee_Info_query.HR_STATUS,
                }

                # Populates admin section
                admin_section = {
                    "manager_flag": employee_Info_query.MANAGER_FLAG,
                    "ebs_user_name": employee_Info_query.HR_EBS_USER_NAME,
                    "review_date": dates.strftime(
                        employee_Info_query.REVIEW_DATE, "%m-%d-%Y %H:%M:%S"
                    )
                    if employee_Info_query.REVIEW_DATE
                    else None,
                }

                # Populates system section
                system_section = {
                    "last_update_date": dates.strftime(
                        employee_Info_query.LAST_UPDATE_DATE, "%m-%d-%Y %H:%M:%S"
                    )
                    if employee_Info_query.LAST_UPDATE_DATE
                    else None,
                    "last_updated_by": employee_Info_query.LAST_UPDATED_BY,
                }

                # Populate ofsc_section
                ofsc_section = fetch_ofsc_details(
                    session, employee_Info_query.HR_RESOURCE_NUMBER
                )

                manager_Info_query = (
                    session.query(
                        tab_hr_tm.EMPLOYEE_NAME,
                        tab_hr_tm.EMPLOYEE_ID,
                        tab_hr_tm.EMAIL,
                        tab_hr_tm.RESOURCE_NUMBER,
                    )
                    # .join(tab_fs_emp, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                    .filter(
                        tab_hr_tm.EMPLOYEE_ID == f"{employee_Info_query.MANAGER_ID}"
                    ).first()
                )

                manager_status_query = (
                    session.query(tab_fs_emp.MANAGER_FLAG)
                    # .join(tab_fs_emp, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                    .filter(
                        tab_fs_emp.EMPLOYEE_ID == f"{employee_Info_query.MANAGER_ID}"
                    ).first()
                )

                if employee_Info_query.EMPLOYEE_ID != None:
                    manager_match_to_hr = None
                else:
                    manager_match_to_hr = "Yes"

                manager_section = {
                    "manager_name": None,
                    "manager_employee_id": None,
                    "email": None,
                    "resource_number": None,
                    "manager_match_to_hr": manager_match_to_hr,
                    "manager_flag": None,
                    "system": {
                        "system_manager_name": employee_Info_query.HR_MANAGER_NAME,
                        "system_manager_employee_id": employee_Info_query.HR_MANAGER_EMPLOYEE_ID,
                    },
                }
                # manager section

                if manager_Info_query:
                    manager_match_to_hr = "Yes"
                    if (
                        manager_Info_query.EMPLOYEE_ID
                        != employee_Info_query.HR_MANAGER_EMPLOYEE_ID
                    ):
                        manager_match_to_hr = "No"

                    manager_section = {
                        "manager_name": manager_Info_query.EMPLOYEE_NAME,
                        "manager_employee_id": manager_Info_query.EMPLOYEE_ID,
                        "email": manager_Info_query.EMAIL,
                        "resource_number": manager_Info_query.RESOURCE_NUMBER,
                        "manager_match_to_hr": manager_match_to_hr,
                        "manager_flag": manager_status_query.MANAGER_FLAG
                        if manager_status_query
                        else "N",
                        "system": {
                            "system_manager_name": employee_Info_query.HR_MANAGER_NAME,
                            "system_manager_employee_id": employee_Info_query.HR_MANAGER_EMPLOYEE_ID,
                        },
                    }

            else:
                employee_section = {
                    "employee_id": None,
                    "employee_name": None,
                    "email": None,
                    "resource_number": None,
                    "admin_notes": None,
                    "alternate_email": None,
                }
                hierarchy_section = {
                    "location_code": None,
                    "area_short_name": None,
                    "region_name": None,
                    "location_match_to_hr": None,
                    "region_status": None,
                    "area_status": None,
                    "system": {
                        "system_region_name": None,
                        "system_area_name": None,
                        "system_area_short_name": None,
                        "system_location_code": None,
                    },
                }
                employee_job_code_section = {
                    "job_id": None,
                    "job_title": None,
                    "job_type": None,
                    "job_adp_code": None,
                    "job_match_to_hr": None,
                    "job_status": None,
                    "system": {
                        "system_job_title": None,
                        "system_job_code": None,
                        "system_job_adp_code": None,
                    },
                }
                service_section = {
                    "business_org": None,
                    "job_type": None,
                    "team_type": None,
                    "team_status": None,
                    "cip": None,
                    "work_shift": None,
                    "on_call": None,
                    "on_site": None,
                    "dedicated": None,
                    "dedicated_to": None,
                    "service_advantage": None,
                    "contingent_worker": None,
                    "fs_status": None,
                    "production_print": None,
                    "service_start_date": None,
                    "service_end_date": None,
                    "record_complete": None,
                }
                hr_status_section = {
                    "actual_termination_date": None,
                    "absence_start_date": None,
                    "absence_end_date": None,
                    "actual_return_to_work": None,
                    "last_hire_date": None,
                    "hr_status": None,
                }
                admin_section = {
                    "manager_flag": None,
                    "ebs_user_name": None,
                    "review_date": None,
                }
                system_section = {"last_update_date": None, "last_updated_by": None}
                manager_section = {
                    "manager_name": None,
                    "manager_employee_id": None,
                    "email": None,
                    "resource_number": None,
                    "manager_match_to_hr": None,
                    "manager_flag": None,
                    "system": {
                        "system_manager_name": None,
                        "system_manager_employee_id": None,
                    },
                }
                ofsc_section = {
                    "status": None,
                    "alternate_email": None,
                    "production_print": None,
                    "last_login": None,
                }

            # Populate hierarchy_details_section
            hierarchy_details_section = fetch_hierarchy_details(session, employee_id)

            response_data = {
                "records": {
                    "employee": employee_section,
                    "hierarchy": hierarchy_section,
                    "manager": manager_section,
                    "employee_job_code": employee_job_code_section,
                    "service": service_section,
                    "hr_status": hr_status_section,
                    "admin": admin_section,
                    "system": system_section,
                    "hierarchy_details": hierarchy_details_section,
                    "ofsc": ofsc_section,
                },
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


def fetch_hierarchy_details(session, employee_id):
    try:
        # Create aliases for database tables
        # tab_fs_emp = initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS
        # tab_hr_tm = initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS
        # tab_area = initialize.db_tables.RAC_FS_TM_AREA
        # tab_region = initialize.db_tables.RAC_FS_TM_REGION
        # Define SQL query
        sql_query = text(
            f"SELECT "
            f"(SELECT CONCAT(EMPLOYEE_ID, ' | ', EMPLOYEE_NAME, ' | ', RESOURCE_NUMBER, ' | ', EMAIL) "
            f"FROM RAC_HR_TM_EMPLOYEE_DTLS WHERE EMPLOYEE_ID = d.REGION_DIR_EMP_ID) AS region_dir_info, "
            f"(SELECT CONCAT(EMPLOYEE_ID, ' | ', EMPLOYEE_NAME, ' | ', RESOURCE_NUMBER, ' | ', EMAIL) "
            f"FROM RAC_HR_TM_EMPLOYEE_DTLS WHERE EMPLOYEE_ID = c.AREA_DIR_EMP_ID) AS area_dir_info, "
            f"(SELECT CONCAT(EMPLOYEE_ID, ' | ', EMPLOYEE_NAME, ' | ', RESOURCE_NUMBER, ' | ', EMAIL) "
            f"FROM RAC_HR_TM_EMPLOYEE_DTLS WHERE EMPLOYEE_ID = c.AREA_FOM_EMP_ID) AS area_fom_info, "
            f"d.REGION_DIR_EMP_ID, c.AREA_DIR_EMP_ID, c.AREA_FOM_EMP_ID "
            f"FROM RAC_FS_TM_EMPLOYEE_DTLS a "
            f"LEFT OUTER JOIN RAC_FS_TM_AREA c ON a.AREA_ID = c.AREA_ID "
            f"LEFT OUTER JOIN RAC_FS_TM_REGION d ON c.REGION_ID = d.REGION_ID "
            f"WHERE a.EMPLOYEE_ID = :employee_id"
        )

        # Execute SQL query
        result = session.execute(sql_query, {"employee_id": employee_id}).fetchone()
        print(result)
        hierarchy_details_section = {}
        if result:
            # Use integer indices to access tuple elements
            region_dir_info = (
                result[0].split(" | ") if result[0] else [None, None, None, None]
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
                result[1].split(" | ") if result[1] else [None, None, None, None]
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
                result[2].split(" | ") if result[2] else [None, None, None, None]
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
        # Populate hierarchy_details_section
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

    except SQLAlchemyError as e:
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


def fetch_ofsc_details(session, resource_number):
    try:
        tab_ofsc = aliased(initialize.db_tables.RAC_FS_TM_OFSC_DTLS)
        query = (
            session.query(
                tab_ofsc.STATUS,
                tab_ofsc.ALTERNATE_EMAIL,
                tab_ofsc.LAST_LOGIN,
                tab_ofsc.PRODUCTION_PRINT,
            )
            .filter(tab_ofsc.RESOURCE_NUMBER == f"{resource_number}")
            .first()
        )
        if query:
            ofsc_section = {
                "status": query.STATUS if query else None,
                "alternate_email": query.ALTERNATE_EMAIL if query else None,
                "production_print": query.PRODUCTION_PRINT if query else None,
                "last_login": dates.strftime(query.LAST_LOGIN, "%m-%d-%Y %H:%M:%S")
                if query.LAST_LOGIN
                else None,
            }
            return ofsc_section

        return {"status": None, "alternate_email": None, "last_login": None}
    except SQLAlchemyError as e:
        return {"status": None, "alternate_email": None, "last_login": None}


# Add new change data, insert into RAC_FS_TM_EMPLOYEE_UPD table
@employee_router.route("/change-request/<int:employee_id>", methods=["PUT"])
@requestValidation.validate
def update(employee_id: int):
    try:
        data = request.json
        if not employee_id:
            error_response = [
                {"status": "Failed", "message": "employee_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        # Start a database session
        with dbSession() as session:
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            current_time = dt.utcnow().strftime("%H:%M:%S")

            # Append current time to the datetime string
            if "change_effective_date" in data:
                data["change_effective_date"] += f"T{current_time}"

            if "service_start_date" in data:
                data["service_start_date"] += f"T{current_time}"

            if "service_end_date" in data:
                data["service_end_date"] += f"T{current_time}"

            if "review_date" in data:
                data["review_date"] += f"T{current_time}"

            if "processed_date" in data:
                data["processed_date"] += f"T{current_time}"

            if "absence_start_date" in data:
                data["absence_start_date"] += f"T{current_time}"

            if "absence_end_date" in data:
                data["absence_end_date"] += f"T{current_time}"

            if "actual_return_to_work" in data:
                data["actual_return_to_work"] += f"T{current_time}"

            data.setdefault("last_edited_date", current_datetime_utc)
            # data.setdefault("last_edited_by", str(employee_id))
            data.setdefault("last_edited_by", data["logged_in_user_id"])
            data["employee_id"] = str(employee_id)
            data["requested_by"] = data["logged_in_user_id"]
            data["alternate_email_old"] = data["alternate_email"]

            service = baseService(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, session)
            _info = service.get_pk_id(employee_id)

            if _info:
                tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
                job_Info_query = (
                    session.query(
                        tab_job_code.JOB_ID,
                        tab_job_code.JOB_TITLE,
                        tab_job_code.JOB_TYPE,
                        tab_job_code.JOB_ADP_CODE,
                    )
                    .filter(tab_job_code.JOB_ID == _info.JOB_ID)
                    .first()
                )
                data["employee_name"] = _info.EMPLOYEE_NAME if _info else None
                data["job_type"] = job_Info_query.JOB_TYPE if job_Info_query else None
                data["hr_status"] = _info.HR_STATUS if _info else None
            # Create an instance of racFsTmEmployeeUpdateCreate
            service = baseService(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, session)
            row = service.create(racFsTmEmployeeUpdateCreate(**data))

            # Procedure call
            if row.CHANGE_ID:
                proc_results = session.execute(
                    text(f"call RAC_FS_TM_EMP_CHANGE_SUBMIT_PROCEDURE({row.CHANGE_ID})")
                )

            response_data = {
                "records": [{"change_id": row.CHANGE_ID}],
                "status": "Success",
                "message": "Record created successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@employee_router.route("/syncup/<int:employee_id>", methods=["PUT"])
@requestValidation.validate
def syncup(employee_id: int):
    try:
        data = request.json
        syncup_type = data.get("syncup_type")
        data["employee_id"] = str(employee_id)
        if not employee_id:
            error_response = [
                {"status": "Failed", "message": "employee_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400
        if not syncup_type:
            error_response = [
                {"status": "Failed", "message": "syncup_type cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        if data["change_effective_date"] == None:
            error_response = [
                {
                    "status": "Failed",
                    "message": "change_effective_date cannot be empty.",
                }
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        if "change_effective_date" in data:
            current_time = dt.utcnow().strftime("%H:%M:%S")
            data["change_effective_date"] += f"T{current_time}"

        # Start a database session
        with dbSession() as session:
            # common query for emp and hr info
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)

            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            # Build the query to fetch manager data
            employee_Info_query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_fs_emp.EMPLOYEE_NAME,
                    tab_fs_emp.MANAGER_ID.label("MANAGER_ID"),
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.AREA_ID.label("AREA_ID"),
                    tab_fs_emp.LOCATION_CODE.label("LOCATION_CODE"),
                    tab_fs_emp.JOB_ID.label("JOB_ID"),
                    tab_fs_emp.TEAM_TYPE_ID.label("TEAM_TYPE_ID"),
                    tab_fs_emp.CIP,
                    tab_fs_emp.WORK_SHIFT,
                    tab_fs_emp.ON_CALL,
                    tab_fs_emp.ON_SITE,
                    tab_fs_emp.DEDICATED,
                    tab_fs_emp.DEDICATED_TO,
                    tab_fs_emp.SERVICE_ADVANTAGE,
                    tab_fs_emp.FS_STATUS,
                    tab_fs_emp.PRODUCTION_PRINT,
                    tab_fs_emp.SERVICE_START_DATE,
                    tab_fs_emp.SERVICE_END_DATE,
                    tab_fs_emp.RECORD_COMPLETE,
                    tab_fs_emp.MANAGER_FLAG,
                    tab_fs_emp.ALTERNATE_EMAIL,
                    tab_fs_emp.BUSINESS_ORG.label("BUSINESS_ORG"),
                    tab_hr_tm.MANAGER_NAME.label("HR_MANAGER_NAME"),
                    tab_hr_tm.MANAGER_EMPLOYEE_ID.label("HR_MANAGER_EMPLOYEE_ID"),
                    tab_hr_tm.EMPLOYEE_NAME.label("HR_EMPLOYEE_NAME"),
                    tab_hr_tm.EMAIL.label("HR_EMAIL"),
                    tab_hr_tm.RESOURCE_NUMBER.label("HR_RESOURCE_NUMBER"),
                    tab_hr_tm.REGION.label("HR_REGION"),
                    tab_hr_tm.AREA.label("HR_AREA"),
                    tab_hr_tm.AREA_SHORT.label("HR_AREA_SHORT"),
                    tab_hr_tm.LOCATION_CODE.label("HR_LOCATION_CODE"),
                    tab_hr_tm.JOB_TITLE.label("HR_JOB_TITLE"),
                    tab_hr_tm.JOB_CODE.label("HR_JOB_CODE"),
                    tab_hr_tm.JOB_ADP.label("HR_JOB_ADP"),
                    tab_hr_tm.JOB_FAMILY.label("HR_JOB_FAMILY"),
                    tab_hr_tm.CONTINGENT_WORKER.label("HR_CONTINGENT_WORKER"),
                    tab_hr_tm.ACTUAL_TERMINATION_DATE.label(
                        "HR_ACTUAL_TERMINATION_DATE"
                    ),
                    tab_fs_emp.ABSENCE_START_DATE.label("HR_ABSENCE_START_DATE"),
                    tab_fs_emp.ABSENCE_END_DATE.label("HR_ABSENCE_END_DATE"),
                    tab_fs_emp.ACTUAL_RETURN_TO_WORK.label("HR_ACTUAL_RETURN_TO_WORK"),
                    tab_hr_tm.ORG_CODE.label("HR_ORG_CODE"),
                    tab_hr_tm.LAST_HIRE_DATE.label("HR_LAST_HIRE_DATE"),
                    tab_hr_tm.EBS_USER_NAME.label("HR_EBS_USER_NAME"),
                    tab_hr_tm.LAST_UPDATE_DATE.label("HR_LAST_UPDATE_DATE"),
                    tab_hr_tm.LAST_UPDATED_BY.label("HR_LAST_UPDATED_BY"),
                    tab_fs_emp.HR_STATUS.label("HR_STATUS"),
                    tab_fs_emp.OFSC_STATUS,
                    tab_fs_emp.REVIEW_DATE,
                )
                .join(tab_hr_tm, tab_hr_tm.EMPLOYEE_ID == tab_fs_emp.EMPLOYEE_ID)
                .filter(tab_fs_emp.EMPLOYEE_ID == employee_id)
                .first()
            )

            if employee_Info_query is None:
                error_response = [
                    {
                        "status": "Failed",
                        "message": "Employee data not found in master record.",
                    }
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 404

            service = baseService(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, session)
            # default values from fs employee table
            tab_team_type = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)
            team_type_Info_query = (
                session.query(tab_team_type.TEAM_TYPE_ID, tab_team_type.TEAM_TYPE_NAME)
                .filter(tab_team_type.TEAM_TYPE_ID == employee_Info_query.TEAM_TYPE_ID)
                .first()
            )

            job_code_tab = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)

            job_code_query = (
                session.query(
                    job_code_tab.JOB_TITLE,
                    job_code_tab.STATUS,
                    job_code_tab.JOB_TYPE,
                    job_code_tab.JOB_ADP_CODE,
                )
                .filter(job_code_tab.JOB_ID == employee_Info_query.JOB_ID)
                .first()
            )

            area_tab = aliased(initialize.db_tables.RAC_FS_TM_AREA)
            region_tab = aliased(initialize.db_tables.RAC_FS_TM_REGION)
            area_query = (
                session.query(region_tab.REGION_NAME, area_tab.AREA_SHORT_NAME)
                .join(region_tab, region_tab.REGION_ID == area_tab.REGION_ID)
                .filter(area_tab.AREA_ID == employee_Info_query.AREA_ID)
                .first()
            )

            data["employee_name"] = employee_Info_query.EMPLOYEE_NAME
            data["hr_status"] = employee_Info_query.HR_STATUS
            data["absence_start_date"] = employee_Info_query.HR_ABSENCE_START_DATE
            data["absence_end_date"] = employee_Info_query.HR_ABSENCE_END_DATE
            data["actual_return_to_work"] = employee_Info_query.HR_ACTUAL_RETURN_TO_WORK
            data["admin_notes"] = employee_Info_query.ADMIN_NOTES
            data["team_type"] = (
                team_type_Info_query.TEAM_TYPE_NAME
                if employee_Info_query.TEAM_TYPE_ID
                else None
            )
            data["cip"] = employee_Info_query.CIP
            data["work_shift"] = employee_Info_query.WORK_SHIFT
            data["on_call"] = employee_Info_query.ON_CALL
            data["on_site"] = employee_Info_query.ON_SITE
            data["dedicated"] = employee_Info_query.DEDICATED
            data["dedicated_to"] = employee_Info_query.DEDICATED_TO
            data["service_advantage"] = employee_Info_query.SERVICE_ADVANTAGE
            data["contingent_worker"] = employee_Info_query.HR_CONTINGENT_WORKER
            data["fs_status"] = employee_Info_query.FS_STATUS
            data["production_print"] = employee_Info_query.PRODUCTION_PRINT
            data["service_start_date"] = employee_Info_query.SERVICE_START_DATE
            data["service_end_date"] = employee_Info_query.SERVICE_END_DATE
            data["record_complete"] = employee_Info_query.RECORD_COMPLETE
            data["manager_flag"] = employee_Info_query.MANAGER_FLAG
            data["business_org"] = employee_Info_query.BUSINESS_ORG

            # data["job_code"] = job_code_query.JOB_CODE
            data["job_title"] = job_code_query.JOB_TITLE
            data["job_adp"] = job_code_query.JOB_ADP_CODE
            data["job_type"] = job_code_query.JOB_TYPE

            data["region"] = area_query.REGION_NAME
            data["area"] = area_query.AREA_SHORT_NAME
            data["loc_code"] = employee_Info_query.LOCATION_CODE

            data["manager_id"] = employee_Info_query.MANAGER_ID

            data["change_note"] = "Sync up"
            data["requested_by"] = data["logged_in_user_id"]
            data["approval_required"] = "Y"
            data["approved"] = "N"
            data["csa_change_comment"] = ""
            data["change_type"] = "SYNCUP"
            data["change_status"] = "Pending"
            data["alternate_email"] = employee_Info_query.ALTERNATE_EMAIL
            data["ofsc_status"] = employee_Info_query.OFSC_STATUS
            data["review_date"] = employee_Info_query.REVIEW_DATE
            data["alternate_email_old"] = employee_Info_query.ALTERNATE_EMAIL

            lv_status = "active"
            if syncup_type == "job":
                hr_job_code_query = (
                    session.query(
                        job_code_tab.JOB_TITLE,
                        job_code_tab.STATUS,
                        job_code_tab.JOB_TYPE,
                        job_code_tab.JOB_ADP_CODE,
                    )
                    .filter(job_code_tab.JOB_ADP_CODE == employee_Info_query.HR_JOB_ADP)
                    .filter(job_code_tab.STATUS.ilike(f"{lv_status}"))
                    .first()
                )
                if hr_job_code_query is None:
                    error_response = [
                        {
                            "status": "Failed",
                            "message": "Job Info can not be inactive or not exists in TM.",
                        }
                    ]
                    return json.loads(APIResponse(errors=error_response).to_json()), 404
                # data["job_code"] = employee_Info_query.HR_JOB_CODE
                data["job_title"] = employee_Info_query.HR_JOB_TITLE
                data["job_adp"] = employee_Info_query.HR_JOB_ADP
                data["attribute1"] = syncup_type
                data["change_note"] = "Sync up - job"
                row = service.create(racFsTmEmployeeUpdateJob(**data))
            elif syncup_type == "hierarchy":
                area_tab_m = aliased(
                    initialize.db_tables.RAC_FS_TM_AREA, name="area_tab_m"
                )
                region_tab_m = aliased(
                    initialize.db_tables.RAC_FS_TM_REGION, name="region_tab_m"
                )
                tab_fs_emp_m = aliased(
                    initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="tab_fs_emp_m"
                )
                m_h_query = (
                    session.query(
                        tab_fs_emp_m.EMPLOYEE_ID,
                        region_tab_m.REGION_NAME,
                        area_tab_m.AREA_SHORT_NAME,
                    )
                    .join(area_tab_m, tab_fs_emp_m.AREA_ID == area_tab_m.AREA_ID)
                    .join(region_tab_m, region_tab_m.REGION_ID == area_tab_m.REGION_ID)
                    .filter(tab_fs_emp_m.EMPLOYEE_ID == employee_Info_query.MANAGER_ID)
                    .filter(area_tab_m.STATUS.ilike(f"{lv_status}"))
                    .filter(region_tab_m.STATUS.ilike(f"{lv_status}"))
                    .first()
                )
                if m_h_query is None:
                    error_response = [
                        {
                            "status": "Failed",
                            "message": "Area and Region Info can not be null or inactive",
                        }
                    ]
                    return json.loads(APIResponse(errors=error_response).to_json()), 404

                data["region"] = m_h_query.REGION_NAME
                data["area"] = m_h_query.AREA_SHORT_NAME
                data["loc_code"] = employee_Info_query.HR_LOCATION_CODE
                data["attribute1"] = syncup_type
                data["change_note"] = "Sync up - hierarchy"
                row = service.create(racFsTmEmployeeUpdateHierarchy(**data))
            elif syncup_type == "manager":
                tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
                _Info = (
                    session.query(tab_fs_emp.EMPLOYEE_ID)
                    .filter(
                        tab_fs_emp.EMPLOYEE_ID
                        == employee_Info_query.HR_MANAGER_EMPLOYEE_ID
                    )
                    .filter(tab_fs_emp.MANAGER_FLAG == "Y")
                    .first()
                )
                if _Info is None:
                    error_response = [
                        {
                            "status": "Failed",
                            "message": "Manager Info can not be null or not exists in TM.",
                        }
                    ]
                    return json.loads(APIResponse(errors=error_response).to_json()), 404
                data["manager_id"] = employee_Info_query.HR_MANAGER_EMPLOYEE_ID
                data["attribute1"] = syncup_type
                data["change_note"] = "Sync up - manager"
                row = service.create(racFsTmEmployeeUpdateManager(**data))
            else:
                error_response = [
                    {
                        "status": "Failed",
                        "message": "syncup_type not matched in our records.",
                    }
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 404

            if row.CHANGE_ID:
                proc_results = session.execute(
                    text(f"call RAC_FS_TM_EMP_CHANGE_SUBMIT_PROCEDURE({row.CHANGE_ID})")
                )

            response_data = {
                "records": [{"change_id": row.CHANGE_ID}],
                "status": "Success",
                "message": "Record created successfully",
            }

            return json.loads(APIResponse(data=response_data).to_json()), 200

    except NoResultFound:
        error_response = [{"status": "Failed", "message": "No records found"}]
        return json.loads(APIResponse(errors=error_response).to_json()), 404

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@employee_router.route("/is_employee_as_manager", methods=["GET"])
@requestValidation.validate
def is_employee_as_manager():
    try:
        employee_id = request.args.get("employee_id")
        if not employee_id:
            error_response = [
                {"status": "Failed", "message": "employee_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            record_count = (
                session.query(tab_fs_emp.EMPLOYEE_ID)
                .filter(tab_fs_emp.MANAGER_ID == employee_id)
                .filter(tab_fs_emp.FS_STATUS.in_(["Active", "LOA"]))
            ).count()

            response_data = {
                "count": record_count,
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@employee_router.route("/is_employee_exists", methods=["GET"])
@requestValidation.validate
def is_employee_exists():
    try:
        employee_id = request.args.get("employee_id")
        if not employee_id:
            error_response = [
                {"status": "Failed", "message": "employee_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)

            fs_em_exists = (
                session.query(tab_fs_emp.EMPLOYEE_ID).filter(
                    tab_fs_emp.EMPLOYEE_ID == employee_id
                )
            ).first()

            if fs_em_exists:
                error_response = {
                    "records": [],
                    "status": "Failed",
                    "message": "Employee already exists in Tech Master.",
                }
                return json.loads(APIResponse(errors=error_response).to_json()), 400

            hr_em_exists = (
                session.query(tab_hr_tm.EMPLOYEE_ID).filter(
                    tab_hr_tm.EMPLOYEE_ID == employee_id
                )
            ).first()

            if hr_em_exists:
                hr_employee_Info_query = (
                    session.query(
                        tab_hr_tm.EMPLOYEE_ID,
                        tab_hr_tm.EMPLOYEE_NAME.label("HR_EMPLOYEE_NAME"),
                        tab_hr_tm.EMAIL.label("HR_EMAIL"),
                        tab_hr_tm.RESOURCE_NUMBER.label("HR_RESOURCE_NUMBER"),
                        tab_hr_tm.ORG_CODE.label("HR_ORG_CODE"),
                        tab_hr_tm.LAST_HIRE_DATE.label("HR_LAST_HIRE_DATE"),
                        tab_hr_tm.HR_STATUS,
                        tab_hr_tm.ABSENCE_START_DATE.label("HR_ABSENCE_START_DATE"),
                        tab_hr_tm.ABSENCE_END_DATE.label("HR_ABSENCE_END_DATE"),
                        tab_hr_tm.ACTUAL_TERMINATION_DATE.label(
                            "HR_ACTUAL_TERMINATION_DATE"
                        ),
                        tab_hr_tm.ACTUAL_RETURN_TO_WORK.label(
                            "HR_ACTUAL_RETURN_TO_WORK"
                        ),
                        tab_hr_tm.JOB_CODE.label("HR_JOB_CODE"),
                        tab_hr_tm.JOB_ADP.label("HR_JOB_ADP"),
                        tab_hr_tm.JOB_TITLE.label("HR_JOB_TITLE"),
                        tab_hr_tm.JOB_FAMILY.label("HR_JOB_FAMILY"),
                        tab_hr_tm.MANAGER_EMPLOYEE_ID.label("HR_MANAGER_EMPLOYEE_ID"),
                        tab_hr_tm.MANAGER_NAME.label("HR_MANAGER_NAME"),
                        tab_hr_tm.AREA.label("HR_AREA"),
                        tab_hr_tm.AREA_SHORT.label("HR_AREA_SHORT"),
                        tab_hr_tm.REGION.label("HR_REGION"),
                        tab_hr_tm.BUSINESS_ORG.label("HR_BUSINESS_ORG"),
                        tab_hr_tm.CONTINGENT_WORKER.label("HR_CONTINGENT_WORKER"),
                        tab_hr_tm.EBS_USER_NAME.label("HR_EBS_USER_NAME"),
                        tab_hr_tm.OIC_FLAG.label("HR_OIC_FLAG"),
                        tab_hr_tm.LAST_UPDATE_DATE.label("HR_LAST_UPDATE_DATE"),
                        tab_hr_tm.LAST_UPDATED_BY.label("HR_LAST_UPDATED_BY"),
                        tab_hr_tm.LOCATION_CODE,
                    )
                    .filter(tab_hr_tm.EMPLOYEE_ID == employee_id)
                    .first()
                )

                if hr_employee_Info_query:
                    employee_section = {
                        "employee_id": hr_employee_Info_query.EMPLOYEE_ID,
                        "employee_name": hr_employee_Info_query.HR_EMPLOYEE_NAME,
                        "email": hr_employee_Info_query.HR_EMAIL,
                        "resource_number": hr_employee_Info_query.HR_RESOURCE_NUMBER,
                        "admin_notes": None,
                        "alternate_email": None,
                    }

                    tab_area_m = aliased(
                        initialize.db_tables.RAC_FS_TM_AREA, name="tab_area_m"
                    )
                    tab_region_m = aliased(
                        initialize.db_tables.RAC_FS_TM_REGION, name="tab_region_m"
                    )
                    tab_fs_emp_m = aliased(
                        initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS,
                        name="tab_fs_emp_m",
                    )

                    manager_hierarchy_query = (
                        session.query(
                            tab_fs_emp_m.EMPLOYEE_ID,
                            tab_area_m.AREA_SHORT_NAME,
                            tab_region_m.REGION_NAME,
                            tab_fs_emp_m.MANAGER_FLAG,
                            tab_area_m.STATUS.label("AREA_STATUS"),
                            tab_region_m.STATUS.label("REGION_STATUS"),
                        )
                        .filter(
                            tab_fs_emp_m.EMPLOYEE_ID
                            == hr_employee_Info_query.HR_MANAGER_EMPLOYEE_ID
                        )
                        .filter(tab_fs_emp_m.MANAGER_FLAG == "Y")
                        .join(tab_area_m, tab_fs_emp_m.AREA_ID == tab_area_m.AREA_ID)
                        .join(
                            tab_region_m, tab_region_m.REGION_ID == tab_area_m.REGION_ID
                        )
                        .first()
                    )

                    # tab_area = aliased(
                    #     initialize.db_tables.RAC_FS_TM_AREA, name="tab_area"
                    # )
                    # tab_region = aliased(
                    #     initialize.db_tables.RAC_FS_TM_REGION, name="tab_region"
                    # )
                    # configuration_Info_query = (
                    #     session.query(
                    #         tab_area.AREA_SHORT_NAME,
                    #         tab_region.REGION_NAME,
                    #         tab_area.STATUS.label("AREA_STATUS"),
                    #         tab_region.STATUS.label("REGION_STATUS"),
                    #     )
                    #     .join(tab_region, tab_region.REGION_ID == tab_area.REGION_ID)
                    #     .filter(
                    #         tab_area.AREA_SHORT_NAME.ilike(
                    #             f"%{hr_employee_Info_query.HR_AREA_SHORT}%"
                    #         )
                    #     )
                    #     .first()
                    # )
                    location_match_to_hr = "No"
                    if manager_hierarchy_query:
                        if (
                            manager_hierarchy_query.REGION_STATUS == "ACTIVE"
                            and manager_hierarchy_query.AREA_STATUS == "ACTIVE"
                        ):
                            location_match_to_hr = "Yes"

                    hierarchy_section = {
                        "location_code": None,
                        "area_short_name": manager_hierarchy_query.AREA_SHORT_NAME
                        if manager_hierarchy_query
                        else None,
                        "region_name": manager_hierarchy_query.REGION_NAME
                        if manager_hierarchy_query
                        else None,
                        "location_match_to_hr": location_match_to_hr
                        if manager_hierarchy_query
                        else "No",
                        "region_status": manager_hierarchy_query.REGION_STATUS
                        if manager_hierarchy_query
                        else None,
                        "area_status": manager_hierarchy_query.AREA_STATUS
                        if manager_hierarchy_query
                        else None,
                        "system": {
                            "system_region_name": manager_hierarchy_query.REGION_NAME
                            if manager_hierarchy_query
                            else None,
                            "system_area_name": manager_hierarchy_query.AREA_SHORT_NAME
                            if manager_hierarchy_query
                            else None,
                            "system_area_short_name": manager_hierarchy_query.AREA_SHORT_NAME
                            if manager_hierarchy_query
                            else None,
                            "system_location_code": None,
                        },
                    }

                    tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)

                    job_Info_query = (
                        session.query(
                            tab_job_code.JOB_ID,
                            tab_job_code.JOB_TITLE,
                            tab_job_code.JOB_TYPE,
                            tab_job_code.JOB_ADP_CODE,
                            tab_job_code.STATUS,
                        )
                        .filter(
                            tab_job_code.JOB_ADP_CODE.ilike(
                                f"%{hr_employee_Info_query.HR_JOB_ADP}%"
                            )
                        )
                        .first()
                    )
                    if job_Info_query:
                        job_match_to_hr = "Yes"
                    else:
                        job_match_to_hr = "No"

                    # Populates Employee Job section
                    employee_job_code_section = {
                        "job_id": job_Info_query.JOB_ID if job_Info_query else None,
                        "job_title": job_Info_query.JOB_TITLE
                        if job_Info_query
                        else None,
                        "job_type": job_Info_query.JOB_TYPE if job_Info_query else None,
                        "job_adp_code": job_Info_query.JOB_ADP_CODE
                        if job_Info_query
                        else None,
                        "job_match_to_hr": job_match_to_hr,
                        "job_status": job_Info_query.STATUS if job_Info_query else None,
                        "system": {
                            "system_job_title": hr_employee_Info_query.HR_JOB_TITLE,
                            "system_job_code": hr_employee_Info_query.HR_JOB_CODE,
                            "system_job_adp_code": hr_employee_Info_query.HR_JOB_ADP,
                        },
                    }

                    # Populates Service Section
                    service_section = {
                        "business_org": hr_employee_Info_query.HR_BUSINESS_ORG
                        if hr_employee_Info_query.HR_BUSINESS_ORG
                        else None,
                        "job_type": job_Info_query.JOB_TYPE if job_Info_query else None,
                        "team_type": None,
                        "team_status": None,
                        "cip": None,
                        "work_shift": None,
                        "on_call": None,
                        "on_site": None,
                        "dedicated": None,
                        "dedicated_to": None,
                        "service_advantage": None,
                        "contingent_worker": hr_employee_Info_query.HR_CONTINGENT_WORKER
                        if hr_employee_Info_query.HR_CONTINGENT_WORKER
                        else None,
                        "fs_status": None,
                        "production_print": None,
                        "service_start_date": None,
                        "service_end_date": None,
                        "record_complete": None,
                    }

                    # Populates HR Status Section
                    hr_status_section = {
                        "actual_termination_date": dates.strftime(
                            hr_employee_Info_query.HR_ACTUAL_TERMINATION_DATE,
                            "%m-%d-%Y",
                        )
                        if hr_employee_Info_query.HR_ACTUAL_TERMINATION_DATE
                        else None,
                        "absence_start_date": dates.strftime(
                            hr_employee_Info_query.HR_ABSENCE_START_DATE, "%m-%d-%Y"
                        )
                        if hr_employee_Info_query.HR_ABSENCE_START_DATE
                        else None,
                        "absence_end_date": dates.strftime(
                            hr_employee_Info_query.HR_ABSENCE_END_DATE, "%m-%d-%Y"
                        )
                        if hr_employee_Info_query.HR_ABSENCE_END_DATE
                        else None,
                        "actual_return_to_work": dates.strftime(
                            hr_employee_Info_query.HR_ACTUAL_RETURN_TO_WORK,
                            "%m-%d-%Y",
                        )
                        if hr_employee_Info_query.HR_ACTUAL_RETURN_TO_WORK
                        else None,
                        "last_hire_date": dates.strftime(
                            hr_employee_Info_query.HR_LAST_HIRE_DATE, "%m-%d-%Y"
                        )
                        if hr_employee_Info_query.HR_LAST_HIRE_DATE
                        else None,
                        "hr_status": hr_employee_Info_query.HR_STATUS,
                    }

                    # Populates admin section
                    admin_section = {
                        "manager_flag": None,
                        "ebs_user_name": hr_employee_Info_query.HR_EBS_USER_NAME,
                        "review_date": None,
                    }

                    # Populates system section
                    system_section = {
                        "last_update_date": dates.strftime(
                            hr_employee_Info_query.HR_LAST_UPDATE_DATE,
                            "%m-%d-%Y %H:%M:%S",
                        )
                        if hr_employee_Info_query.HR_LAST_UPDATE_DATE
                        else None,
                        "last_updated_by": hr_employee_Info_query.HR_LAST_UPDATED_BY,
                    }

                    # Populate ofsc_section
                    ofsc_section = fetch_ofsc_details(
                        session, hr_employee_Info_query.HR_RESOURCE_NUMBER
                    )

                    manager_Info_query = (
                        session.query(
                            tab_hr_tm.EMPLOYEE_NAME,
                            tab_hr_tm.EMPLOYEE_ID,
                            tab_hr_tm.EMAIL,
                            tab_hr_tm.RESOURCE_NUMBER,
                        )
                        .filter(
                            tab_hr_tm.EMPLOYEE_ID
                            == hr_employee_Info_query.HR_MANAGER_EMPLOYEE_ID
                        )
                        .first()
                    )

                    manager_tm_Info_query = (
                        session.query(tab_fs_emp.MANAGER_FLAG)
                        .filter(
                            tab_fs_emp.EMPLOYEE_ID
                            == hr_employee_Info_query.HR_MANAGER_EMPLOYEE_ID
                        )
                        .first()
                    )
                    manager_match_to_hr = "No"
                    if manager_tm_Info_query:
                        if manager_tm_Info_query.MANAGER_FLAG == "Y":
                            manager_match_to_hr = "Yes"

                    manager_section = {
                        "manager_name": manager_Info_query.EMPLOYEE_NAME
                        if manager_Info_query
                        else None,
                        "manager_employee_id": manager_Info_query.EMPLOYEE_ID
                        if manager_Info_query
                        else None,
                        "email": manager_Info_query.EMAIL
                        if manager_Info_query
                        else None,
                        "resource_number": manager_Info_query.RESOURCE_NUMBER
                        if manager_Info_query
                        else None,
                        "manager_match_to_hr": manager_match_to_hr
                        if manager_Info_query
                        else None,
                        "manager_flag": manager_tm_Info_query.MANAGER_FLAG
                        if manager_tm_Info_query
                        else None,
                        "system": {
                            "system_manager_name": manager_Info_query.EMPLOYEE_NAME
                            if manager_Info_query
                            else None,
                            "system_manager_employee_id": manager_Info_query.EMPLOYEE_ID
                            if manager_Info_query
                            else None,
                        },
                    }

                else:
                    employee_section = {
                        "employee_id": None,
                        "employee_name": None,
                        "email": None,
                        "resource_number": None,
                        "admin_notes": None,
                        "alternate_email": None,
                    }
                    hierarchy_section = {
                        "location_code": None,
                        "area_short_name": None,
                        "region_name": None,
                        "location_match_to_hr": None,
                        "region_status": None,
                        "area_status": None,
                        "system": {
                            "system_region_name": None,
                            "system_area_name": None,
                            "system_area_short_name": None,
                            "system_location_code": None,
                        },
                    }
                    employee_job_code_section = {
                        "job_id": None,
                        "job_title": None,
                        "job_type": None,
                        "job_adp_code": None,
                        "job_match_to_hr": None,
                        "job_status": None,
                        "system": {
                            "system_job_title": None,
                            "system_job_code": None,
                            "system_job_adp_code": None,
                        },
                    }
                    service_section = {
                        "business_org": None,
                        "job_type": None,
                        "team_type": None,
                        "team_status": None,
                        "cip": None,
                        "work_shift": None,
                        "on_call": None,
                        "on_site": None,
                        "dedicated": None,
                        "dedicated_to": None,
                        "service_advantage": None,
                        "contingent_worker": None,
                        "fs_status": None,
                        "production_print": None,
                        "service_start_date": None,
                        "service_end_date": None,
                        "record_complete": None,
                    }
                    hr_status_section = {
                        "actual_termination_date": None,
                        "absence_start_date": None,
                        "absence_end_date": None,
                        "actual_return_to_work": None,
                        "last_hire_date": None,
                        "hr_status": None,
                    }
                    admin_section = {
                        "manager_flag": None,
                        "ebs_user_name": None,
                        "review_date": None,
                    }
                    system_section = {"last_update_date": None, "last_updated_by": None}
                    manager_section = {
                        "manager_name": None,
                        "manager_employee_id": None,
                        "email": None,
                        "resource_number": None,
                        "manager_match_to_hr": None,
                        "manager_flag": None,
                        "system": {
                            "system_manager_name": None,
                            "system_manager_employee_id": None,
                        },
                    }
                    ofsc_section = {
                        "status": None,
                        "alternate_email": None,
                        "production_print": None,
                        "last_login": None,
                    }

                # Populate hierarchy_details_section
                hierarchy_details_section = fetch_hierarchy_details(
                    session, employee_id
                )

                response_data = {
                    "records": {
                        "employee": employee_section,
                        "hierarchy": hierarchy_section,
                        "manager": manager_section,
                        "employee_job_code": employee_job_code_section,
                        "service": service_section,
                        "hr_status": hr_status_section,
                        "admin": admin_section,
                        "system": system_section,
                        "hierarchy_details": hierarchy_details_section,
                        "ofsc": ofsc_section,
                    },
                    "status": "Success",
                    "message": "Data retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200

            else:
                error_response = {
                    "records": [],
                    "status": "Failed",
                    "message": "Employee not exists in HRMS. Please contact support team.",
                }
                return json.loads(APIResponse(errors=error_response).to_json()), 400

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@employee_router.route("/add-employee/<int:employee_id>", methods=["PUT"])
@requestValidation.validate
def addEmployee(employee_id: int):
    try:
        data = request.json
        if not employee_id:
            error_response = [
                {"status": "Failed", "message": "employee_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        # Start a database session
        with dbSession() as session:
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            current_time = dt.utcnow().strftime("%H:%M:%S")

            # Append current time to the datetime string
            if "change_effective_date" in data:
                data["change_effective_date"] += f"T{current_time}"

            if "service_start_date" in data:
                data["service_start_date"] += f"T{current_time}"

            if "service_end_date" in data:
                data["service_end_date"] += f"T{current_time}"

            if "review_date" in data:
                data["review_date"] += f"T{current_time}"

            if "processed_date" in data:
                data["processed_date"] += f"T{current_time}"

            if "absence_start_date" in data:
                data["absence_start_date"] += f"T{current_time}"

            if "absence_end_date" in data:
                data["absence_end_date"] += f"T{current_time}"

            if "actual_return_to_work" in data:
                data["actual_return_to_work"] += f"T{current_time}"

            if "processed_date" in data:
                data["processed_date"] += f"T{current_time}"

            data.setdefault("last_edited_date", current_datetime_utc)
            # data.setdefault("last_edited_by", str(employee_id))
            data.setdefault("last_edited_by", data["logged_in_user_id"])
            data["employee_id"] = str(employee_id)
            data["requested_by"] = data["logged_in_user_id"]
            data["approved"] = "N"
            data["approval_required"] = "Y"
            data["change_type"] = "ADD"
            data["change_status"] = "Pending"
            # data["team_type"] = "Commercial"
            # data["fs_status"] = "Inactive"
            data["csa_change_comment"] = "New Employee Add"
            data["csa_notification_required"] = "Y"

            service = baseService(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, session)
            _info = service.get_pk_id(employee_id)

            if _info:
                tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
                job_Info_query = (
                    session.query(
                        tab_job_code.JOB_ID,
                        tab_job_code.JOB_TITLE,
                        tab_job_code.JOB_TYPE,
                        tab_job_code.JOB_ADP_CODE,
                    )
                    .filter(tab_job_code.JOB_ADP_CODE.ilike(f"%{data['job_adp']}%"))
                    .first()
                )
                data["employee_name"] = _info.EMPLOYEE_NAME if _info else None
                data["job_type"] = job_Info_query.JOB_TYPE if job_Info_query else None
                data["hr_status"] = _info.HR_STATUS if _info else None
            # Create an instance of racFsTmEmployeeUpdateCreate
            service = baseService(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, session)
            row = service.create(racFsTmEmployeeUpdateCreate(**data))

            # if row.CHANGE_ID:
            #     proc_results = session.execute(
            #         text(f"call RAC_FS_TM_EMP_CHANGE_SUBMIT_PROCEDURE({row.CHANGE_ID})")
            #     )

            response_data = {
                "records": [{"change_id": row.CHANGE_ID}],
                "status": "Success",
                "message": "Record created successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
