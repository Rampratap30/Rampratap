import json
import os
from datetime import date as dates
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy import and_, desc, func, null, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.components.email.main import send_email_csa
from app.components.employee.main import fetch_hierarchy_details, fetch_ofsc_details
from app.lib.aws.aws_lambda import awsLambda
from app.lib.aws.aws_s3 import awsS3Upload
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_employee_dtls import racFsTmEmployeeDtlsSchema
from app.lib.core.schemas.rac_fs_tm_employee_update import racFsTmEmployeeUpdateSchema
from app.lib.core.schemas.rac_fs_tm_logs import racFsTmLogsCreate
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

changes_router = Blueprint("changes", __name__)


# This endpoint will be used for the changes page filter section.
@changes_router.route("/get", methods=["POST"])
@requestValidation.validate
def get_change_dashboard():
    try:
        data = request.json
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_emp_upd = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, name="upd"
            )
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="fs"
            )
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hr")
            tab_hrm_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrm"
            )

            # Build the query to fetch data
            query = (
                session.query(
                    tab_emp_upd.CHANGE_ID.label("CHANGE_ID"),
                    func.coalesce(tab_fs_emp.EMPLOYEE_ID, tab_hr_tm.EMPLOYEE_ID).label(
                        "EMPLOYEE_ID"
                    ),
                    tab_hr_tm.EMPLOYEE_NAME.label("EMPLOYEE_NAME"),
                    tab_hr_tm.HR_STATUS.label("HR_STATUS"),
                    func.coalesce(
                        tab_hrm_tm.EMPLOYEE_NAME, tab_hr_tm.MANAGER_NAME
                    ).label("MANAGER_NAME"),
                    tab_emp_upd.CHANGE_EFFECTIVE_DATE.label("CHANGE_EFFECTIVE_DATE"),
                    func.RAC_FS_TM_GET_USER_NAME(tab_emp_upd.REQUESTED_BY).label(
                        "REQUESTED_BY"
                    ),
                    tab_emp_upd.CHANGE_STATUS.label("CHANGE_STATUS"),
                    tab_emp_upd.CHANGE_NOTE.label("CHANGE_NOTE"),
                    tab_emp_upd.ATTRIBUTE1.label("SYNCUP_TYPE"),
                    tab_emp_upd.FS_STATUS.label("FS_STATUS"),
                    tab_emp_upd.ADMIN_NOTES.label("ADMIN_NOTES"),
                    tab_emp_upd.BUSINESS_ORG.label("BUSINESS_ORG"),
                )
                .join(tab_hr_tm, tab_hr_tm.EMPLOYEE_ID == tab_emp_upd.EMPLOYEE_ID)
                .outerjoin(
                    tab_fs_emp, tab_fs_emp.EMPLOYEE_ID == tab_emp_upd.EMPLOYEE_ID
                )
                .outerjoin(
                    tab_hrm_tm,
                    tab_hrm_tm.EMPLOYEE_ID
                    == func.coalesce(tab_fs_emp.MANAGER_ID, tab_emp_upd.MANAGER_ID),
                )
                .filter(tab_emp_upd.REQUESTED_BY != "AWS-ONE-TIME")
            )

            if data["is_export_all"] != "Y":
                # Apply filtering based on manager_name if provided
                if data["manager_name"]:
                    query = query.filter(
                        tab_hrm_tm.EMPLOYEE_NAME.ilike(f'%{data["manager_name"]}%')
                    )
                if data["q"]:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.ilike(f'%{data["q"]}%'),
                            tab_hr_tm.EMPLOYEE_NAME.ilike(f'%{data["q"]}%'),
                            tab_hr_tm.EMPLOYEE_ID.ilike(f'%{data["q"]}%'),
                        )
                    )

                if data["status"]:
                    query = query.filter(
                        tab_emp_upd.CHANGE_STATUS
                        == func.coalesce(data["status"], tab_emp_upd.CHANGE_STATUS)
                    )

                if data["change_id"]:
                    query = query.filter(
                        tab_emp_upd.CHANGE_ID
                        == func.coalesce(data["change_id"], tab_emp_upd.CHANGE_ID)
                    )

                if data["requested_by"]:
                    query = query.filter(
                        (func.RAC_FS_TM_GET_USER_NAME(tab_emp_upd.REQUESTED_BY)).ilike(
                            f'%{data["requested_by"]}%'
                        )
                    )

                # print(data["request_type"])
                # if data["request_type"].upper() == "ALL":
                #    query = query.filter(
                #        tab_emp_upd.REQUESTED_BY == data["employee_id"]
                #    )
                if data["request_type"].upper() == "ALL PENDING":
                    query = query.filter(tab_emp_upd.CHANGE_STATUS == "Pending")
                if data["request_type"].upper() == "MY PENDING":
                    query = query.filter(
                        and_(
                            tab_emp_upd.REQUESTED_BY == data["logged_in_user_id"],
                            tab_emp_upd.CHANGE_STATUS == "Pending",
                        )
                    )

                if (data["from_date"]) and (data["to_date"]):
                    date = datetime.strptime(data["to_date"], "%Y-%m-%d")
                    # endDate = date + timedelta(days=1)
                    query = query.filter(
                        tab_emp_upd.CHANGE_EFFECTIVE_DATE.between(
                            data["from_date"] + " 00:00:00",
                            data["to_date"] + " 23:59:59",
                        )
                    )
                total_items = query.count()

                if data["order_by"] == "status":
                    data["order_by"] = "CHANGE_STATUS"

                # Apply sorting based on order_by and order
                query = query.order_by(
                    (
                        text(str(data["order_by"]).upper())
                        if data["order_by"] and data["order"] != "desc"
                        else None
                    ),
                    (
                        text(f'{str(data["order_by"]).upper()} desc')
                        if data["order_by"] and data["order"] == "desc"
                        else None
                    ),
                )
                # Fetch the results with pagination
                results = (
                    query.offset((data["page"] - 1) * data["per_page"])
                    .limit(data["per_page"])
                    .all()
                )
            else:
                total_items = query.count()
                results = query.all()

            response_data = {
                "records": [
                    {
                        "change_id": result.CHANGE_ID,
                        "employee_id": result.EMPLOYEE_ID,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "change_effective_date": (
                            dates.strftime(result.CHANGE_EFFECTIVE_DATE, "%m/%d/%Y")
                            if result.CHANGE_EFFECTIVE_DATE
                            else None
                        ),
                        "requested_by": result.REQUESTED_BY,
                        "status": result.CHANGE_STATUS,
                        "change_note": result.CHANGE_NOTE,
                        "syncup_type": result.SYNCUP_TYPE,
                        "fs_status": result.FS_STATUS,
                        "hr_status":result.HR_STATUS,
                        "admin_notes": result.ADMIN_NOTES,
                        "business_org":result.BUSINESS_ORG,
                    }
                    for result in results
                ],
                "total_items": total_items,
                "page": data["page"],
                "per_page": data["per_page"],
                "order_by": data["order_by"],
                "order": data["order"],
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@changes_router.route("/change-info", methods=["GET"])
@requestValidation.validate
def change_info():
    try:
        change_id = request.args.get("change_id")
        if not change_id:
            error_response = [
                {"status": "Failed", "message": "change_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_emp_upd = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD)
            tab_region = aliased(
                initialize.db_tables.RAC_FS_TM_REGION, name="tab_region_m"
            )
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="tab_area_m")

            employee_update_info = (
                session.query(
                    tab_emp_upd.EMPLOYEE_ID,
                    tab_emp_upd.MANAGER_FLAG,
                    tab_emp_upd.REVIEW_DATE,
                    tab_emp_upd.JOB_FAMILY,
                    tab_emp_upd.JOB_TITLE,
                    # tab_emp_upd.JOB_CODE,
                    tab_emp_upd.JOB_ADP,
                    tab_emp_upd.LOC_CODE,
                    tab_emp_upd.REGION,
                    tab_emp_upd.AREA,
                    tab_emp_upd.MANAGER_ID,
                    tab_emp_upd.TEAM_TYPE,
                    tab_emp_upd.WORK_SHIFT,
                    tab_emp_upd.ON_CALL,
                    tab_emp_upd.ON_SITE,
                    tab_emp_upd.DEDICATED,
                    tab_emp_upd.DEDICATED_TO,
                    tab_emp_upd.SERVICE_ADVANTAGE,
                    tab_emp_upd.FS_STATUS,
                    tab_emp_upd.SERVICE_START_DATE,
                    tab_emp_upd.SERVICE_END_DATE,
                    tab_emp_upd.RECORD_COMPLETE,
                    tab_emp_upd.CHANGE_ID,
                    tab_emp_upd.CHANGE_EFFECTIVE_DATE,
                    tab_emp_upd.CHANGE_TYPE,
                    tab_emp_upd.CHANGE_NOTE,
                    tab_emp_upd.CHANGE_STATUS,
                    func.RAC_FS_TM_GET_USER_NAME(tab_emp_upd.REQUESTED_BY).label(
                        "REQUESTED_BY"
                    ),
                    tab_emp_upd.REQUESTED_BY.label("REQUESTED_BY_ID"),
                    tab_emp_upd.APPROVAL_REQUIRED,
                    tab_emp_upd.APPROVED,
                    func.RAC_FS_TM_GET_USER_NAME(tab_emp_upd.APPROVED_BY).label(
                        "APPROVED_BY"
                    ),
                    tab_emp_upd.CSA_NOTIFICATION_REQUIRED,
                    tab_emp_upd.CSA_CHANGE_COMMENT,
                    tab_emp_upd.CSA_NOTIFICATION_COMPLETE,
                    tab_emp_upd.LAST_EDITED_DATE,
                    func.RAC_FS_TM_GET_USER_NAME(tab_emp_upd.LAST_EDITED_BY).label(
                        "LAST_EDITED_BY"
                    ),
                    tab_emp_upd.PROCESSED_DATE,
                    tab_emp_upd.ALTERNATE_EMAIL,
                    tab_emp_upd.ADMIN_NOTES,
                    tab_emp_upd.BUSINESS_ORG,
                    tab_emp_upd.ABSENCE_START_DATE.label("HR_ABSENCE_START_DATE"),
                    tab_emp_upd.ABSENCE_END_DATE.label("HR_ABSENCE_END_DATE"),
                    tab_emp_upd.ACTUAL_RETURN_TO_WORK.label("HR_ACTUAL_RETURN_TO_WORK"),
                    tab_emp_upd.CREATION_DATE,
                    tab_emp_upd.JOB_TYPE,
                    tab_emp_upd.PRODUCTION_PRINT,
                    tab_emp_upd.HR_STATUS,
                )
                .filter(tab_emp_upd.CHANGE_ID == change_id)
                .first()
            )

            if employee_update_info is None:
                error_response = [{"status": "Failed", "message": "No Records found."}]
                return json.loads(APIResponse(errors=error_response).to_json()), 500

            if (
                employee_update_info.REQUESTED_BY == "HR"
                and employee_update_info.CHANGE_TYPE == "ADD"
            ):
                employee_Info_query = (
                    session.query(
                        tab_hr_tm.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                        tab_hr_tm.EMPLOYEE_NAME,
                        tab_hr_tm.EMAIL,
                        tab_hr_tm.RESOURCE_NUMBER,
                        null().label("ADMIN_NOTES"),
                        tab_hr_tm.ACTUAL_TERMINATION_DATE.label(
                            "HR_ACTUAL_TERMINATION_DATE"
                        ),
                        # tab_hr_tm.ABSENCE_START_DATE.label("HR_ABSENCE_START_DATE"),
                        # tab_hr_tm.ABSENCE_END_DATE.label("HR_ABSENCE_END_DATE"),
                        # tab_hr_tm.ACTUAL_RETURN_TO_WORK.label("HR_ACTUAL_RETURN_TO_WORK"),
                        tab_hr_tm.LAST_HIRE_DATE.label("HR_LAST_HIRE_DATE"),
                        tab_hr_tm.HR_STATUS,
                        tab_hr_tm.LAST_UPDATE_DATE.label("HR_LAST_UPDATE_DATE"),
                        tab_hr_tm.LAST_UPDATED_BY.label("HR_LAST_UPDATED_BY"),
                        tab_hr_tm.EBS_USER_NAME,
                        tab_hr_tm.CONTINGENT_WORKER.label("HR_CONTINGENT_WORKER"),
                    )
                    .filter(tab_hr_tm.EMPLOYEE_ID == employee_update_info.EMPLOYEE_ID)
                    .first()
                )
            else:
                employee_Info_query = (
                    session.query(
                        tab_fs_emp.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                        tab_hr_tm.EMPLOYEE_NAME,
                        tab_hr_tm.EMAIL,
                        tab_hr_tm.RESOURCE_NUMBER,
                        tab_fs_emp.ADMIN_NOTES,
                        tab_hr_tm.ACTUAL_TERMINATION_DATE.label(
                            "HR_ACTUAL_TERMINATION_DATE"
                        ),
                        # tab_hr_tm.ABSENCE_START_DATE.label("HR_ABSENCE_START_DATE"),
                        # tab_hr_tm.ABSENCE_END_DATE.label("HR_ABSENCE_END_DATE"),
                        # tab_hr_tm.ACTUAL_RETURN_TO_WORK.label("HR_ACTUAL_RETURN_TO_WORK"),
                        tab_hr_tm.LAST_HIRE_DATE.label("HR_LAST_HIRE_DATE"),
                        tab_hr_tm.HR_STATUS,
                        tab_hr_tm.LAST_UPDATE_DATE.label("HR_LAST_UPDATE_DATE"),
                        tab_hr_tm.LAST_UPDATED_BY.label("HR_LAST_UPDATED_BY"),
                        tab_hr_tm.EBS_USER_NAME,
                        tab_hr_tm.CONTINGENT_WORKER.label("HR_CONTINGENT_WORKER"),
                    )
                    .join(tab_hr_tm, tab_hr_tm.EMPLOYEE_ID == tab_fs_emp.EMPLOYEE_ID)
                    .filter(tab_fs_emp.EMPLOYEE_ID == employee_update_info.EMPLOYEE_ID)
                    .first()
                )

            employee_section = {
                "employee_id": None,
                "employee_name": None,
                "email": None,
                "alternate_email": employee_update_info.ALTERNATE_EMAIL,
                "resource_number": None,
                "admin_notes": employee_update_info.ADMIN_NOTES,
            }

            lv_ebs_user_name = None

            if employee_Info_query:
                employee_section = {
                    "employee_id": employee_Info_query.EMPLOYEE_ID,
                    "employee_name": employee_Info_query.EMPLOYEE_NAME,
                    "email": employee_Info_query.EMAIL,
                    "alternate_email": employee_update_info.ALTERNATE_EMAIL,
                    "resource_number": employee_Info_query.RESOURCE_NUMBER,
                    "admin_notes": employee_update_info.ADMIN_NOTES,
                }
                lv_ebs_user_name = employee_Info_query.EBS_USER_NAME

            else:
                hr_employee_Info_query = (
                    session.query(
                        tab_hr_tm.EMPLOYEE_ID,
                        tab_hr_tm.EMPLOYEE_NAME,
                        tab_hr_tm.EMAIL,
                        tab_hr_tm.RESOURCE_NUMBER,
                        tab_hr_tm.ACTUAL_TERMINATION_DATE.label(
                            "HR_ACTUAL_TERMINATION_DATE"
                        ),
                        tab_hr_tm.LAST_HIRE_DATE.label("HR_LAST_HIRE_DATE"),
                        tab_hr_tm.HR_STATUS,
                        tab_hr_tm.LAST_UPDATE_DATE.label("HR_LAST_UPDATE_DATE"),
                        tab_hr_tm.LAST_UPDATED_BY.label("HR_LAST_UPDATED_BY"),
                        tab_hr_tm.EBS_USER_NAME,
                        tab_hr_tm.CONTINGENT_WORKER.label("HR_CONTINGENT_WORKER"),
                    )
                    .filter(tab_hr_tm.EMPLOYEE_ID == employee_update_info.EMPLOYEE_ID)
                    .first()
                )
                if hr_employee_Info_query:
                    employee_section = {
                        "employee_id": hr_employee_Info_query.EMPLOYEE_ID,
                        "employee_name": hr_employee_Info_query.EMPLOYEE_NAME,
                        "email": hr_employee_Info_query.EMAIL,
                        "alternate_email": employee_update_info.ALTERNATE_EMAIL,
                        "resource_number": hr_employee_Info_query.RESOURCE_NUMBER,
                        "admin_notes": employee_update_info.ADMIN_NOTES,
                    }
                    lv_ebs_user_name = hr_employee_Info_query.EBS_USER_NAME

            # Populates admin section
            admin_section = {
                "manager_flag": employee_update_info.MANAGER_FLAG,
                "review_date": (
                    dates.strftime(
                        employee_update_info.REVIEW_DATE, "%m-%d-%Y %H:%M:%S"
                    )
                    if employee_update_info.REVIEW_DATE
                    else None
                ),
                "ebs_user_name": lv_ebs_user_name,
            }
            # Populates Employee Job section
            tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
            res_job_id = (
                session.query(tab_job_code.JOB_ID, tab_job_code.STATUS)
                # .filter(
                #    tab_job_code.JOB_CODE.ilike(f"%{employee_update_info.JOB_CODE}%")
                # )
                .filter(
                    tab_job_code.JOB_ADP_CODE.ilike(f"%{employee_update_info.JOB_ADP}%")
                )
            ).first()

            employee_job_code_section = {
                "job_id": res_job_id.JOB_ID if res_job_id else None,
                "job_title": employee_update_info.JOB_TITLE,
                # "job_code": employee_update_info.JOB_CODE,
                "job_adp_code": employee_update_info.JOB_ADP,
                "job_type": employee_update_info.JOB_TYPE,
                "job_status": res_job_id.STATUS if res_job_id else None,
            }
            # Populate hierarchy_section
            region_status_query = (
                session.query(
                    tab_region.STATUS.label("REGION_STATUS"),
                )
                .filter(tab_region.REGION_NAME == employee_update_info.REGION)
                .first()
            )
            area_status_query = (
                session.query(
                    tab_area.STATUS.label("AREA_STATUS"),
                )
                .filter(tab_area.AREA_SHORT_NAME == employee_update_info.AREA)
                .first()
            )
            hierarchy_section = {
                "location_code": employee_update_info.LOC_CODE,
                "region_name": employee_update_info.REGION,
                "region_status": (
                    region_status_query.REGION_STATUS if region_status_query else None
                ),
                "area_short_name": employee_update_info.AREA,
                "area_status": (
                    area_status_query.AREA_STATUS if area_status_query else None
                ),
            }
            # Populates HR Status Section
            actual_termination_date = None
            last_hire_date = None
            hr_status = None
            if employee_Info_query:
                actual_termination_date = (
                    dates.strftime(
                        employee_Info_query.HR_ACTUAL_TERMINATION_DATE, "%m-%d-%Y"
                    )
                    if employee_Info_query.HR_ACTUAL_TERMINATION_DATE
                    else None
                )
                last_hire_date = (
                    dates.strftime(employee_Info_query.HR_LAST_HIRE_DATE, "%m-%d-%Y")
                    if employee_Info_query.HR_LAST_HIRE_DATE
                    else None
                )
                hr_status = employee_Info_query.HR_STATUS

            hr_status_section = {
                "actual_termination_date": actual_termination_date,
                "absence_start_date": (
                    dates.strftime(
                        employee_update_info.HR_ABSENCE_START_DATE, "%m-%d-%Y"
                    )
                    if employee_update_info.HR_ABSENCE_START_DATE
                    else None
                ),
                "absence_end_date": (
                    dates.strftime(employee_update_info.HR_ABSENCE_END_DATE, "%m-%d-%Y")
                    if employee_update_info.HR_ABSENCE_END_DATE
                    else None
                ),
                "actual_return_to_work": (
                    dates.strftime(
                        employee_update_info.HR_ACTUAL_RETURN_TO_WORK, "%m-%d-%Y"
                    )
                    if employee_update_info.HR_ACTUAL_RETURN_TO_WORK
                    else None
                ),
                "last_hire_date": last_hire_date,
                "hr_status": hr_status,
            }
            # manager section
            manager_Info_query = (
                session.query(
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.EMPLOYEE_ID.label("MANAGER_EMP_ID"),
                    tab_hr_tm.EMAIL,
                    tab_hr_tm.RESOURCE_NUMBER,
                )
                .filter(tab_hr_tm.EMPLOYEE_ID == employee_update_info.MANAGER_ID)
                .first()
            )

            manager_status_query = (
                session.query(tab_fs_emp.MANAGER_FLAG)
                # .join(tab_fs_emp, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .filter(
                    tab_fs_emp.EMPLOYEE_ID == employee_update_info.MANAGER_ID
                ).first()
            )

            if manager_Info_query:
                manager_section = {
                    "manager_name": manager_Info_query.EMPLOYEE_NAME,
                    "manager_employee_id": manager_Info_query.MANAGER_EMP_ID,
                    "email": manager_Info_query.EMAIL,
                    "resource_number": manager_Info_query.RESOURCE_NUMBER,
                    "manager_flag": (
                        manager_status_query.MANAGER_FLAG
                        if manager_status_query
                        else "N"
                    ),
                }
            else:
                manager_section = {}

            # Populate ofsc_section
            RN = employee_Info_query.RESOURCE_NUMBER if employee_Info_query else None
            ofsc_section = fetch_ofsc_details(session, RN)
            last_update_date = None
            last_update_by = None
            if employee_Info_query:
                last_update_date = (
                    dates.strftime(
                        employee_Info_query.HR_LAST_UPDATE_DATE, "%m-%d-%Y %H:%M:%S"
                    )
                    if employee_Info_query.HR_LAST_UPDATE_DATE
                    else None
                )
                last_update_by = employee_Info_query.HR_LAST_UPDATED_BY
            # Populates system section
            last_update_date = None
            last_update_by = None

            if employee_Info_query:
                last_update_date = (
                    dates.strftime(
                        employee_Info_query.HR_LAST_UPDATE_DATE, "%m-%d-%Y %H:%M:%S"
                    )
                    if employee_Info_query.HR_LAST_UPDATE_DATE
                    else None
                )
                last_update_by = employee_Info_query.HR_LAST_UPDATED_BY
            system_section = {
                "last_update_date": last_update_date,
                "last_updated_by": last_update_by,
            }

            tab_team_type = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)

            team_type_Info_query = (
                session.query(
                    tab_team_type.TEAM_TYPE_ID,
                    tab_team_type.TEAM_TYPE_NAME,
                    tab_team_type.STATUS,
                )
                .filter(tab_team_type.TEAM_TYPE_NAME == employee_update_info.TEAM_TYPE)
                .first()
            )

            contingent_worker = None
            if employee_Info_query:
                contingent_worker = employee_Info_query.HR_CONTINGENT_WORKER
            elif hr_employee_Info_query:
                contingent_worker = hr_employee_Info_query.HR_CONTINGENT_WORKER

            # Populates Service Section
            service_section = {
                "business_org": (
                    employee_update_info.BUSINESS_ORG
                    if employee_update_info.BUSINESS_ORG
                    else None
                ),
                "team_type": (
                    employee_update_info.TEAM_TYPE
                    if employee_update_info.TEAM_TYPE
                    else None
                ),
                "team_status": (
                    team_type_Info_query.STATUS if team_type_Info_query else None
                ),
                "work_shift": (
                    employee_update_info.WORK_SHIFT
                    if employee_update_info.WORK_SHIFT
                    else None
                ),
                "on_call": (
                    employee_update_info.ON_CALL
                    if employee_update_info.ON_CALL
                    else None
                ),
                "on_site": (
                    employee_update_info.ON_SITE
                    if employee_update_info.ON_SITE
                    else None
                ),
                "dedicated": (
                    employee_update_info.DEDICATED
                    if employee_update_info.DEDICATED
                    else None
                ),
                "dedicated_to": (
                    employee_update_info.DEDICATED_TO
                    if employee_update_info.DEDICATED_TO
                    else None
                ),
                "service_advantage": (
                    employee_update_info.SERVICE_ADVANTAGE
                    if employee_update_info.SERVICE_ADVANTAGE
                    else None
                ),
                "fs_status": (
                    employee_update_info.FS_STATUS
                    if employee_update_info.FS_STATUS
                    else None
                ),
                "service_start_date": (
                    dates.strftime(employee_update_info.SERVICE_START_DATE, "%m-%d-%Y")
                    if employee_update_info.SERVICE_START_DATE
                    else None
                ),
                "service_end_date": (
                    dates.strftime(employee_update_info.SERVICE_END_DATE, "%m-%d-%Y")
                    if employee_update_info.SERVICE_END_DATE
                    else None
                ),
                "record_complete": (
                    employee_update_info.RECORD_COMPLETE
                    if employee_update_info.RECORD_COMPLETE
                    else None
                ),
                "production_print": (
                    employee_update_info.PRODUCTION_PRINT
                    if employee_update_info.PRODUCTION_PRINT
                    else None
                ),
                "contingent_worker": contingent_worker,
            }

            # Populate hierarchy_details_section
            hierarchy_details_section = fetch_hierarchy_details(
                session, employee_update_info.EMPLOYEE_ID
            )

            # Populates change system section
            change_system_section = {
                "change_id": employee_update_info.CHANGE_ID,
                "change_effective_date": (
                    dates.strftime(
                        employee_update_info.CHANGE_EFFECTIVE_DATE, "%m-%d-%Y"
                    )
                    if employee_update_info.CHANGE_EFFECTIVE_DATE
                    else None
                ),
                "change_type": employee_update_info.CHANGE_TYPE,
                "change_note": employee_update_info.CHANGE_NOTE,
                "change_status": employee_update_info.CHANGE_STATUS,
                "requested_by": employee_update_info.REQUESTED_BY,
                "requested_by_id": employee_update_info.REQUESTED_BY_ID,
                "approval_required": employee_update_info.APPROVAL_REQUIRED,
                "approved": employee_update_info.APPROVED,
                "approved_by": employee_update_info.APPROVED_BY,
                "csa_notification_required": employee_update_info.CSA_NOTIFICATION_REQUIRED,
                "csa_change_comment": employee_update_info.CSA_CHANGE_COMMENT,
                "csa_notification_complete": employee_update_info.CSA_NOTIFICATION_COMPLETE,
                "last_edited_date": (
                    dates.strftime(employee_update_info.LAST_EDITED_DATE, "%m-%d-%Y")
                    if employee_update_info.LAST_EDITED_DATE
                    else None
                ),
                "last_edited_by": employee_update_info.LAST_EDITED_BY,
                "processed_date": (
                    dates.strftime(employee_update_info.PROCESSED_DATE, "%m-%d-%Y")
                    if employee_update_info.PROCESSED_DATE
                    else None
                ),
                "creation_date": (
                    dates.strftime(employee_update_info.CREATION_DATE, "%m-%d-%Y")
                    if employee_update_info.CREATION_DATE
                    else None
                ),
            }

            response_data = {
                "records": {
                    "admin": admin_section,
                    "employee": employee_section,
                    "employee_job_code": employee_job_code_section,
                    "hierarchy": hierarchy_section,
                    "hierarchy_details": hierarchy_details_section,
                    "hr_status": hr_status_section,
                    "manager": manager_section,
                    "ofsc": ofsc_section,
                    "service": service_section,
                    "system": system_section,
                    "change_system": change_system_section,
                },
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@changes_router.route("/pre-change-id", methods=["GET"])
@requestValidation.validate
def pre_change_info():
    try:
        change_id = request.args.get("change_id")
        employee_id = request.args.get("employee_id")
        if not change_id:
            error_response = [
                {"status": "Failed", "message": "change_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_emp_upd = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD)
            change_info = (
                (
                    session.query(tab_emp_upd.CHANGE_ID)
                    .filter(tab_emp_upd.EMPLOYEE_ID == employee_id)
                    .filter(tab_emp_upd.CHANGE_STATUS == "Processed")
                    .filter(tab_emp_upd.CHANGE_ID < change_id)
                )
                .order_by(text("CHANGE_ID desc"))
                .first()
            )

            response_data = {
                "records": {
                    "change_id": change_info.CHANGE_ID if change_info else "",
                },
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Bulk approved
@changes_router.route("/bulk-approved", methods=["PUT"])
@requestValidation.validate
def bulk_approved():
    try:
        data = request.json
        if "change_id" not in data or "logged_in_user_id" not in data:
            error_response = [
                {"status": "Failed", "message": "ID field cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400
        change_ids = data["change_id"]
        logged_in_user_id = data["logged_in_user_id"]

        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, session)
            # current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            current_datetime_utc = datetime.utcnow()
            sql_get_name = text(
                f"SELECT RAC_FS_TM_GET_USER_NAME (:employee_id) AS USER_NAME"
            )

            for change_id in change_ids:
                update_query = session.query(service.model).filter(
                    service.model.CHANGE_ID == change_id
                )
                # upd_result = update_query.first()

                update_query.update(
                    {
                        "CHANGE_STATUS": "Approved",
                        "APPROVED": "Y",
                        "APPROVED_BY": logged_in_user_id,
                        "LAST_UPDATE_DATE": current_datetime_utc,
                        "LAST_UPDATED_BY": logged_in_user_id,
                    },
                    # synchronize_session=False,
                )
                session.commit()
                upd_result = update_query.first()

                if (
                    upd_result.CHANGE_EFFECTIVE_DATE is None
                    or upd_result.CHANGE_EFFECTIVE_DATE <= dt.utcnow()
                ):
                    empService = baseService(
                        initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, session
                    )
                    emp_update_query = session.query(empService.model).filter(
                        empService.model.EMPLOYEE_ID == upd_result.EMPLOYEE_ID
                    )
                    emp_update_result = emp_update_query.first()

                    tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
                    tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
                    tab_team_type = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)

                    res_area_id = (
                        session.query(
                            tab_area.AREA_ID, tab_area.AREA_SHORT_NAME
                        ).filter(tab_area.AREA_SHORT_NAME.ilike(f"%{upd_result.AREA}%"))
                    ).first()

                    res_job_id = (
                        session.query(tab_job_code.JOB_ID, tab_job_code.JOB_TITLE)
                        # .filter(tab_job_code.JOB_CODE.ilike(f"%{upd_result.JOB_CODE}%"))
                        .filter(
                            tab_job_code.JOB_ADP_CODE.ilike(f"%{upd_result.JOB_ADP}%")
                        )
                    ).first()

                    res_team_type_id = (
                        session.query(
                            tab_team_type.TEAM_TYPE_ID, tab_team_type.TEAM_TYPE_NAME
                        ).filter(
                            tab_team_type.TEAM_TYPE_NAME.ilike(
                                f"%{upd_result.TEAM_TYPE}%"
                            )
                        )
                    ).first()

                    lv_new_hire = "N"
                    # new hire logic
                    if emp_update_result is None:
                        insert_stmt = initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS.__table__.insert().values(
                            {
                                "EMPLOYEE_ID": upd_result.EMPLOYEE_ID,
                                "EMPLOYEE_NAME": upd_result.EMPLOYEE_NAME,
                                "AREA_ID": res_area_id.AREA_ID,
                                "LOCATION_CODE": upd_result.LOC_CODE,
                                "MANAGER_ID": upd_result.MANAGER_ID,
                                "MANAGER_FLAG": upd_result.MANAGER_FLAG,
                                "JOB_ID": res_job_id.JOB_ID,
                                "TEAM_TYPE_ID": res_team_type_id.TEAM_TYPE_ID,
                                "WORK_SHIFT": upd_result.WORK_SHIFT,
                                "ON_CALL": upd_result.ON_CALL,
                                "ON_SITE": upd_result.ON_SITE,
                                "DEDICATED": upd_result.DEDICATED,
                                "DEDICATED_TO": upd_result.DEDICATED_TO,
                                "BUSINESS_ORG": upd_result.BUSINESS_ORG,
                                "SERVICE_ADVANTAGE": upd_result.SERVICE_ADVANTAGE,
                                "SERVICE_START_DATE": upd_result.SERVICE_START_DATE,
                                "SERVICE_END_DATE": upd_result.SERVICE_END_DATE,
                                "FS_STATUS": upd_result.FS_STATUS,
                                "RECORD_COMPLETE": upd_result.RECORD_COMPLETE,
                                "MANAGER_FLAG": upd_result.MANAGER_FLAG,
                                "ADMIN_NOTES": upd_result.ADMIN_NOTES,
                                # "ALTERNATE_EMAIL": upd_result.ALTERNATE_EMAIL,
                                "LAST_UPDATE_DATE": current_datetime_utc,
                                "LAST_UPDATED_BY": logged_in_user_id,
                                "ABSENCE_START_DATE": upd_result.ABSENCE_START_DATE,
                                "ABSENCE_END_DATE": upd_result.ABSENCE_END_DATE,
                                "ACTUAL_RETURN_TO_WORK": upd_result.ACTUAL_RETURN_TO_WORK,
                                "ALTERNATE_EMAIL": upd_result.ALTERNATE_EMAIL,
                                "PRODUCTION_PRINT": upd_result.PRODUCTION_PRINT,
                                "OFSC_STATUS": upd_result.OFSC_STATUS,
                                "RECORD_COMPLETE": upd_result.RECORD_COMPLETE,
                                "HR_STATUS": upd_result.HR_STATUS,
                                "REVIEW_DATE": upd_result.REVIEW_DATE,
                            }
                        )
                        session.execute(insert_stmt)
                        session.commit()
                        lv_new_hire = "Y"

                    emp_update_result = emp_update_query.first()

                    hierarchy = fetch_hierarchy_details(
                        session, emp_update_result.EMPLOYEE_ID
                    )

                    sql_query = text(
                        f"SELECT"
                        f" EMP.RESOURCE_NUMBER,"
                        f" FS_EMP.EMPLOYEE_NAME,"
                        f" REGION.REGION_NAME,"
                        f" AREA.AREA_SHORT_NAME,"
                        f" MGR.EMPLOYEE_NAME AS MANAGER_NAME,"
                        f" MGR.RESOURCE_NUMBER AS MANAGER_RESOURCE_NUMBER,"
                        f" TEAM.TEAM_TYPE_NAME,"
                        f" JOB.JOB_TITLE,"
                        f" EMP.ACTUAL_TERMINATION_DATE,"
                        f" FS_EMP.HR_STATUS,"
                        f" FS_EMP.ALTERNATE_EMAIL,"
                        f" EMP.EMAIL,"
                        f" MGR.EMAIL AS MANAGER_EMAIL"
                        f" FROM"
                        f" RAC_FS_TM_EMPLOYEE_DTLS FS_EMP"
                        f" JOIN"
                        f" RAC_HR_TM_EMPLOYEE_DTLS EMP ON EMP.EMPLOYEE_ID = FS_EMP.EMPLOYEE_ID"
                        f" LEFT JOIN"
                        f" RAC_HR_TM_EMPLOYEE_DTLS MGR ON FS_EMP.MANAGER_ID = MGR.EMPLOYEE_ID"
                        f" LEFT JOIN"
                        f" RAC_FS_TM_AREA AREA ON AREA.AREA_ID = FS_EMP.AREA_ID"
                        f" LEFT JOIN"
                        f" RAC_FS_TM_REGION REGION ON REGION.REGION_ID = AREA.REGION_ID"
                        f" LEFT JOIN"
                        f" RAC_FS_TM_TEAM_TYPE TEAM ON TEAM.TEAM_TYPE_ID = FS_EMP.TEAM_TYPE_ID"
                        f" LEFT JOIN"
                        f" RAC_FS_TM_JOB_CODE JOB ON JOB.JOB_ID = FS_EMP.JOB_ID"
                        f" WHERE"
                        f" FS_EMP.EMPLOYEE_ID = :employee_id"
                    )
                    # Execute SQL query
                    old_result = session.execute(
                        sql_query, {"employee_id": emp_update_result.EMPLOYEE_ID}
                    ).fetchone()

                    last_updated_name = session.execute(
                        sql_get_name, {"employee_id": emp_update_result.LAST_UPDATED_BY}
                    ).first()

                    old_data = {
                        "CSA_CHANGE_COMMENT": None,
                        "LAST_UPDATE_DATE": (
                            emp_update_result.LAST_UPDATE_DATE
                            if lv_new_hire == "N"
                            else None
                        ),
                        "LAST_UPDATED_BY": (
                            last_updated_name.USER_NAME if lv_new_hire == "N" else None
                        ),
                        "CREATION_DATE": (
                            emp_update_result.CREATION_DATE
                            if lv_new_hire == "N"
                            else None
                        ),
                        "CHANGE_TYPE": None,
                        "EMPLOYEE_ID": (
                            emp_update_result.EMPLOYEE_ID
                            if lv_new_hire == "N"
                            else None
                        ),
                        "RESOURCE_NUMBER": (
                            old_result.RESOURCE_NUMBER if lv_new_hire == "N" else None
                        ),
                        "EMPLOYEE_NAME": (
                            old_result.EMPLOYEE_NAME if lv_new_hire == "N" else None
                        ),
                        "EMAIL": old_result.EMAIL if lv_new_hire == "N" else None,
                        "FS_STATUS": (
                            emp_update_result.FS_STATUS if lv_new_hire == "N" else None
                        ),
                        "REGION": (
                            old_result.REGION_NAME if lv_new_hire == "N" else None
                        ),
                        "AREA": (
                            old_result.AREA_SHORT_NAME if lv_new_hire == "N" else None
                        ),
                        "LOC_CODE": (
                            emp_update_result.LOCATION_CODE
                            if lv_new_hire == "N"
                            else None
                        ),
                        "MANAGER_RESOURCE_NUMBER": (
                            old_result.MANAGER_RESOURCE_NUMBER
                            if lv_new_hire == "N"
                            else None
                        ),
                        "MANAGER_NAME": (
                            old_result.MANAGER_NAME if lv_new_hire == "N" else None
                        ),
                        "MANAGER_EMAIL": (
                            old_result.MANAGER_EMAIL if lv_new_hire == "N" else None
                        ),
                        "AREA_DIR_NAME": (
                            hierarchy["area_dir_employee_name"]
                            if lv_new_hire == "N"
                            else None
                        ),
                        "AREA_DIR_EMAIL": (
                            hierarchy["area_dir_email"] if lv_new_hire == "N" else None
                        ),
                        "TEAM_TYPE": (
                            old_result.TEAM_TYPE_NAME if lv_new_hire == "N" else None
                        ),
                        "ALTERNATE_EMAIL": (
                            old_result.ALTERNATE_EMAIL if lv_new_hire == "N" else None
                        ),
                        "JOB_TITLE": (
                            old_result.JOB_TITLE if lv_new_hire == "N" else None
                        ),
                        "ACTUAL_TERMINATION_DATE": (
                            old_result.ACTUAL_TERMINATION_DATE
                            if lv_new_hire == "N"
                            else None
                        ),
                        "APPROVED_BY": None,
                        "CHANGE_NOTE": None,
                        "HR_STATUS": (
                            old_result.HR_STATUS if lv_new_hire == "N" else None
                        ),
                        "REQUESTED_BY": None,
                        "ABSENCE_START_DATE": (
                            emp_update_result.ABSENCE_START_DATE
                            if lv_new_hire == "N"
                            else None
                        ),
                        "ABSENCE_END_DATE": (
                            emp_update_result.ABSENCE_END_DATE
                            if lv_new_hire == "N"
                            else None
                        ),
                    }

                    if upd_result.ATTRIBUTE1 == "manager":
                        emp_update_query.update(
                            {
                                "MANAGER_ID": upd_result.MANAGER_ID,
                                "LAST_UPDATE_DATE": current_datetime_utc,
                                "LAST_UPDATED_BY": logged_in_user_id,
                                "REVIEW_DATE": upd_result.REVIEW_DATE,
                            }
                        )
                    elif upd_result.ATTRIBUTE1 == "job":
                        emp_update_query.update(
                            {
                                "JOB_ID": res_job_id.JOB_ID,
                                "LAST_UPDATE_DATE": current_datetime_utc,
                                "LAST_UPDATED_BY": logged_in_user_id,
                                "REVIEW_DATE": upd_result.REVIEW_DATE,
                            }
                        )
                    elif upd_result.ATTRIBUTE1 == "hierarchy":
                        emp_update_query.update(
                            {
                                "AREA_ID": res_area_id.AREA_ID,
                                "LAST_UPDATE_DATE": current_datetime_utc,
                                "LAST_UPDATED_BY": logged_in_user_id,
                                "REVIEW_DATE": upd_result.REVIEW_DATE,
                            }
                        )
                    else:
                        emp_update_query.update(
                            {
                                "EMPLOYEE_NAME": upd_result.EMPLOYEE_NAME,
                                "AREA_ID": res_area_id.AREA_ID,
                                "LOCATION_CODE": upd_result.LOC_CODE,
                                "MANAGER_ID": upd_result.MANAGER_ID,
                                "JOB_ID": res_job_id.JOB_ID,
                                "TEAM_TYPE_ID": res_team_type_id.TEAM_TYPE_ID,
                                "WORK_SHIFT": upd_result.WORK_SHIFT,
                                "ON_CALL": upd_result.ON_CALL,
                                "ON_SITE": upd_result.ON_SITE,
                                "DEDICATED": upd_result.DEDICATED,
                                "DEDICATED_TO": upd_result.DEDICATED_TO,
                                "BUSINESS_ORG": upd_result.BUSINESS_ORG,
                                "SERVICE_ADVANTAGE": upd_result.SERVICE_ADVANTAGE,
                                "SERVICE_START_DATE": upd_result.SERVICE_START_DATE,
                                "SERVICE_END_DATE": upd_result.SERVICE_END_DATE,
                                "FS_STATUS": upd_result.FS_STATUS,
                                "RECORD_COMPLETE": upd_result.RECORD_COMPLETE,
                                "MANAGER_FLAG": upd_result.MANAGER_FLAG,
                                "ADMIN_NOTES": upd_result.ADMIN_NOTES,
                                "ALTERNATE_EMAIL": upd_result.ALTERNATE_EMAIL,
                                "LAST_UPDATE_DATE": current_datetime_utc,
                                "LAST_UPDATED_BY": logged_in_user_id,
                                "ABSENCE_START_DATE": upd_result.ABSENCE_START_DATE,
                                "ABSENCE_END_DATE": upd_result.ABSENCE_END_DATE,
                                "ACTUAL_RETURN_TO_WORK": upd_result.ACTUAL_RETURN_TO_WORK,
                                "HR_STATUS": upd_result.HR_STATUS,
                                "REVIEW_DATE": upd_result.REVIEW_DATE,
                                "OFSC_STATUS": upd_result.OFSC_STATUS,
                                "PRODUCTION_PRINT": upd_result.PRODUCTION_PRINT,
                            }
                        )

                    update_query.update(
                        {
                            "CHANGE_STATUS": "Processed",
                            "PROCESSED_DATE": current_datetime_utc,
                            "LAST_UPDATE_DATE": current_datetime_utc,
                            "LAST_UPDATED_BY": logged_in_user_id,
                        },
                        # synchronize_session=False,
                    )
                    if upd_result.CSA_NOTIFICATION_REQUIRED == "Y":
                        tab_notify = aliased(initialize.db_tables.RAC_FS_TM_NOTIF)
                        res_email_id = (
                            session.query(tab_notify.EMAIL_ID)
                            .filter(tab_notify.NOTIFICATION_NAME == "CSA Notifications")
                            .filter(tab_notify.STATUS == "ACTIVE")
                        ).all()
                        if res_email_id:
                            sql_query = text(
                                f"SELECT "
                                f" EMP.RESOURCE_NUMBER,"
                                f" FS_EMP.EMPLOYEE_NAME,"
                                f" MGR.EMPLOYEE_NAME as MANAGER_NAME,"
                                f" MGR.RESOURCE_NUMBER as MANAGER_RESOURCE_NUMBER,"
                                f" EMP.ACTUAL_TERMINATION_DATE,"
                                f" FS_EMP.HR_STATUS,"
                                f" EMP.EMAIL,"
                                f" MGR.EMAIL AS MANAGER_EMAIL"
                                f" FROM"
                                f" RAC_FS_TM_EMPLOYEE_UPD FS_EMP"
                                f" JOIN"
                                f" RAC_HR_TM_EMPLOYEE_DTLS EMP ON EMP.EMPLOYEE_ID = FS_EMP.EMPLOYEE_ID"
                                f" LEFT JOIN"
                                f" RAC_HR_TM_EMPLOYEE_DTLS MGR ON FS_EMP.MANAGER_ID = MGR.EMPLOYEE_ID"
                                f" WHERE"
                                f" FS_EMP.CHANGE_ID = :change_id"
                            )
                            # Execute SQL query
                            new_result = session.execute(
                                sql_query, {"change_id": upd_result.CHANGE_ID}
                            ).fetchone()

                            last_updated_name_new = session.execute(
                                sql_get_name,
                                {"employee_id": upd_result.LAST_UPDATED_BY},
                            ).first()

                            approved_by_name = session.execute(
                                sql_get_name, {"employee_id": upd_result.APPROVED_BY}
                            ).first()

                            requested_by_name = session.execute(
                                sql_get_name, {"employee_id": upd_result.REQUESTED_BY}
                            ).first()

                            _formatted_last_update_date = (
                                upd_result.LAST_UPDATE_DATE.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )
                                if upd_result.LAST_UPDATE_DATE
                                else None
                            )

                            new_data = {
                                "CSA_CHANGE_COMMENT": upd_result.CSA_CHANGE_COMMENT,
                                "LAST_UPDATE_DATE": _formatted_last_update_date,
                                "LAST_UPDATED_BY": last_updated_name_new.USER_NAME,
                                "CREATION_DATE": upd_result.CREATION_DATE,
                                "CHANGE_TYPE": upd_result.CHANGE_TYPE,
                                "EMPLOYEE_ID": upd_result.EMPLOYEE_ID,
                                "RESOURCE_NUMBER": new_result.RESOURCE_NUMBER,
                                "EMPLOYEE_NAME": new_result.EMPLOYEE_NAME,
                                "EMAIL": new_result.EMAIL,
                                "FS_STATUS": upd_result.FS_STATUS,
                                "REGION": upd_result.REGION,
                                "AREA": upd_result.AREA,
                                "LOC_CODE": upd_result.LOC_CODE,
                                "MANAGER_RESOURCE_NUMBER": new_result.MANAGER_RESOURCE_NUMBER,
                                "MANAGER_NAME": new_result.MANAGER_NAME,
                                "MANAGER_EMAIL": new_result.MANAGER_EMAIL,
                                "AREA_DIR_NAME": hierarchy["area_dir_employee_name"],
                                "AREA_DIR_EMAIL": hierarchy["area_dir_email"],
                                "TEAM_TYPE": upd_result.TEAM_TYPE,
                                "ALTERNATE_EMAIL": upd_result.ALTERNATE_EMAIL,
                                "JOB_TITLE": upd_result.JOB_TITLE,
                                "ACTUAL_TERMINATION_DATE": new_result.ACTUAL_TERMINATION_DATE,
                                "APPROVED_BY": approved_by_name.USER_NAME,
                                "CHANGE_NOTE": upd_result.CHANGE_NOTE,
                                "HR_STATUS": new_result.HR_STATUS,
                                "REQUESTED_BY": requested_by_name.USER_NAME,
                                "ABSENCE_START_DATE": upd_result.ABSENCE_START_DATE,
                                "ABSENCE_END_DATE": upd_result.ABSENCE_END_DATE,
                            }
                            recipient_email = [(res.EMAIL_ID) for res in res_email_id]
                            send_email_csa(recipient_email, old_data, new_data)
                            update_query.update(
                                {"CSA_NOTIFICATION_COMPLETE": "Y"},
                                # synchronize_session=False,
                            )

            # Commit the changes to the database
            # session.commit()
            response_data = {
                "records": [{"change_id": change_ids}],
                "status": "Success",
                "message": "Change's approved successfully",
            }
        return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Bulk approved
@changes_router.route("/bulk-rejected", methods=["PUT"])
@requestValidation.validate
def bulk_rejected():
    try:
        data = request.json
        change_ids = data["change_id"]
        logged_in_user_id = data["logged_in_user_id"]
        if not change_ids:
            error_response = [
                {"status": "Failed", "message": "change_id list cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, session)
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            for change_id in change_ids:
                session.query(service.model).filter(
                    service.model.CHANGE_ID == change_id
                ).update(
                    {
                        "CHANGE_STATUS": "Rejected",
                        "APPROVED": "N",
                        "APPROVED_BY": logged_in_user_id,
                        "LAST_UPDATE_DATE": current_datetime_utc,
                        "LAST_UPDATED_BY": logged_in_user_id,
                    },
                    synchronize_session=False,
                )

            # Commit the changes to the database
            session.commit()

            response_data = {
                "records": [{"change_id": change_ids}],
                "status": "Success",
                "message": "Change's rejected successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@changes_router.route("/update/<int:change_id>", methods=["PUT"])
@requestValidation.validate
def change_request_update(change_id: int):
    try:
        data = request.json
        if not change_id:
            error_response = [
                {"status": "Failed", "message": "change_id cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        # Start a database session
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, session)
            _info = service.get_pk_id(change_id)

            if _info:
                current_time = dt.utcnow().strftime("%H:%M:%S")
                data["employee_id"] = _info.EMPLOYEE_ID
                data["employee_name"] = _info.EMPLOYEE_NAME
                data["area"] = data["area_short_name"]
                data["production_print"] = _info.PRODUCTION_PRINT
                data["ofsc_status"] = _info.OFSC_STATUS
                data["hr_status"] = _info.HR_STATUS
                data["alternate_email"] = _info.ALTERNATE_EMAIL
                data["csa_change_comment"] = _info.CSA_CHANGE_COMMENT
                data["csa_notification_required"] = _info.CSA_NOTIFICATION_REQUIRED
                data["requested_by"] = _info.REQUESTED_BY
                data["change_type"] = _info.CHANGE_TYPE
                data["attribute1"] = _info.ATTRIBUTE1
                data["attribute2"] = _info.ATTRIBUTE2
                data["attribute3"] = _info.ATTRIBUTE3
                data["attribute4"] = _info.ATTRIBUTE4
                data["attribute5"] = _info.ATTRIBUTE5

                current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                data["last_edited_date"] = current_datetime_utc
                data["last_edited_by"] = str(data["logged_in_user_id"])

                # Append current time to the datetime string
                current_time = dt.utcnow().strftime("%H:%M:%S")
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

                # if "job_code" in data:
                #    data["job_code"] = str(data["job_code"])

                # Create an instance of racFsTmEmployeeUpdateSchema
                row = service.update(_info, racFsTmEmployeeUpdateSchema(**data))

                if row.CHANGE_ID:
                    proc_results = session.execute(
                        text(
                            f"call RAC_FS_TM_EMP_CHANGE_SUBMIT_PROCEDURE({row.CHANGE_ID})"
                        )
                    )

                response_data = {
                    "records": [{"change_id": row.CHANGE_ID}],
                    "status": "Success",
                    "message": "Record updated successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Records not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@changes_router.route("/bulk_import", methods=["POST"])
@requestValidation.validate
def bulk_import():
    try:
        inp_data = request.json
        email_id = inp_data["logged_in_email_id"]
        # Start a database session
        with dbSession() as session:
            if email_id:
                timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

                data = {
                    "lambda_status": "pending",
                    "email_id": email_id,
                    "file_name": inp_data["file_name"],
                    "msg": inp_data["msg"],
                    "type": inp_data["type"],
                    "logged_in_user_id": inp_data["logged_in_user_id"],
                }
                print(data)
                service = baseService(initialize.db_tables.RAC_FS_TM_LOGS, session)
                row = service.create(racFsTmLogsCreate(**data))
                response_data = {
                    "records": [{"log_id": row.TM_LOG_ID}],
                    "status": "Success",
                    "message": "Import details will be shared via email. Approximate time: 15 mins",
                }
                log_details: dict = {"log_id": row.TM_LOG_ID}
            else:
                error_response = [
                    {
                        "status": "Failed",
                        "message": "Email Id not exists in the payload",
                    }
                ]
                return (
                    json.loads(APIResponse(errors=error_response).to_json()),
                    404,
                )
        lambdaName = os.getenv("AWS_LAMBDA_IMPORT")
        lambda_status = awsLambda.invoke_function(lambdaName, log_details, False)
        print(lambda_status)
        return (
            json.loads(APIResponse(data=response_data).to_json()),
            201,
        )

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
