import json
import os
from datetime import date as dates
from datetime import datetime

from flask import Blueprint, request
from sqlalchemy import desc, func, or_, select, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.aws.aws_lambda import awsLambda
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_employee_update import racFsTmEmployeeUpdateCreate
from app.lib.core.schemas.rac_fs_tm_logs import racFsTmLogsCreate
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

home_router = Blueprint("home", __name__)

# This endpoint will be used for the home page filter section.
# It can be used in the manager search popup.


@home_router.route("/get_manager_list", methods=["GET"])
@requestValidation.validate
def get_manager_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        manager_name = request.args.get("manager_name")
        is_export_all = request.args.get("is_export_all", "N")

        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)

            # Build the query to fetch manager data
            query = (
                session.query(
                    tab_hr_tm.EMPLOYEE_NAME.label("EMPLOYEE_NAME"),
                    tab_hr_tm.RESOURCE_NUMBER.label("RESOURCE_NUMBER"),
                    tab_fs_emp.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                )
                .filter(tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .filter(tab_fs_emp.MANAGER_FLAG == "Y")
            )

            # Apply filtering based on manager_name if provided
            total_items = 0
            if is_export_all != "Y":
                if manager_name:
                    query = query.filter(
                        tab_hr_tm.EMPLOYEE_NAME.ilike(f"%{manager_name}%")
                    )

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by.upper()) if order_by and order != "desc" else None,
                    text(f"{order_by.upper()} desc")
                    if order_by and order == "desc"
                    else None,
                )

                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()

            else:
                query = query.order_by(
                    text(order_by.upper()) if order_by and order != "desc" else None,
                    text(f"{order_by.upper()} desc")
                    if order_by and order == "desc"
                    else None,
                )
                total_items = query.count()
                results = query.all()

            response_data = {
                "records": [
                    {
                        "manager_name": result.EMPLOYEE_NAME,
                        "manager_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                    }
                    for result in results
                ],
                "total_items": total_items,
                "page": page,
                "per_page": per_page,
                "order_by": order_by,
                "order": order,
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# This endpoint will be used for the home page filter section.
# It can be used in the employee search popup.
# Filtering will work on these criteria (employee id, employee name, resource name).


@home_router.route("/get_employee_list", methods=["GET"])
@requestValidation.validate
def get_employee_list():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "EMPLOYEE_NAME")
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        manager_name = request.args.get("manager_name")
        change_screen = request.args.get("change_screen")

        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="racTmFsEmp"
            )
            tab_fs_emp_upd = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, name="racTmFsEmp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="racTmHrEmp"
            )
            tab_hr_tm_1 = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="racTmHrEmp1"
            )

            # Build the query to fetch employee data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                    tab_hr_tm.EMPLOYEE_NAME.label("EMPLOYEE_NAME"),
                    tab_hr_tm.RESOURCE_NUMBER.label("RESOURCE_NUMBER"),
                    tab_fs_emp.MANAGER_ID.label("MANAGER_ID"),
                    tab_hr_tm_1.EMPLOYEE_NAME.label("MANAGER_NAME"),
                ).join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                # .join(tab_fs_emp_1, tab_fs_emp.MANAGER_ID == tab_fs_emp_1.EMPLOYEE_ID)
                .outerjoin(
                    tab_hr_tm_1, tab_fs_emp.MANAGER_ID == tab_hr_tm_1.EMPLOYEE_ID
                )
                # .filter(tab_fs_emp.EMPLOYEE_ID != tab_fs_emp.MANAGER_ID)
            )

            if change_screen == "Y":
                query1 = (
                    session.query(
                        tab_hr_tm.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                        tab_hr_tm.EMPLOYEE_NAME.label("EMPLOYEE_NAME"),
                        tab_hr_tm.RESOURCE_NUMBER.label("RESOURCE_NUMBER"),
                        tab_fs_emp.MANAGER_ID.label("MANAGER_ID"),
                        tab_hr_tm_1.EMPLOYEE_NAME.label("MANAGER_NAME"),
                    ).join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                    # .join(tab_fs_emp_1, tab_fs_emp.MANAGER_ID == tab_fs_emp_1.EMPLOYEE_ID)
                    .outerjoin(
                        tab_hr_tm_1, tab_fs_emp.MANAGER_ID == tab_hr_tm_1.EMPLOYEE_ID
                    )
                    # .filter(tab_fs_emp.EMPLOYEE_ID != tab_fs_emp.MANAGER_ID)
                )
                query2 = (
                    session.query(
                        tab_hr_tm.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                        tab_hr_tm.EMPLOYEE_NAME.label("EMPLOYEE_NAME"),
                        tab_hr_tm.RESOURCE_NUMBER.label("RESOURCE_NUMBER"),
                        tab_fs_emp_upd.MANAGER_ID.label("MANAGER_ID"),
                        tab_hr_tm_1.EMPLOYEE_NAME.label("MANAGER_NAME"),
                    )
                    .join(
                        tab_fs_emp_upd,
                        tab_fs_emp_upd.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID,
                    )
                    .outerjoin(
                        tab_hr_tm_1,
                        tab_fs_emp_upd.MANAGER_ID == tab_hr_tm_1.EMPLOYEE_ID,
                    )
                    .filter(tab_fs_emp_upd.CHANGE_TYPE == "ADD")
                    .filter(tab_fs_emp_upd.CHANGE_STATUS != "Processed")
                )
                if q:
                    query1 = query1.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.ilike(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.ilike(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.ilike(f"%{q}%"),
                        )
                    )
                    query2 = query2.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.ilike(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.ilike(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.ilike(f"%{q}%"),
                        )
                    ).distinct()
                query = query1.union(query2).distinct()

            # Apply filtering based on manager_name if provided
            if manager_name:
                query = query.filter(
                    tab_hr_tm_1.EMPLOYEE_NAME.ilike(f"%{manager_name}%")
                )

            if q:
                query = query.filter(
                    or_(
                        tab_hr_tm.RESOURCE_NUMBER.ilike(f"%{q}%"),
                        tab_hr_tm.EMPLOYEE_NAME.ilike(f"%{q}%"),
                        tab_hr_tm.EMPLOYEE_ID.ilike(f"%{q}%"),
                    )
                )

            total_items = query.count()

            # Apply sorting based on order_by and order
            query = query.order_by(
                text(order_by.upper()) if order_by and order != "desc" else None,
                text(f"{order_by.upper()} desc")
                if order_by and order == "desc"
                else None,
            )

            # Fetch the results with pagination
            results = query.offset((page - 1) * per_page).limit(per_page).all()

            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_id": result.MANAGER_ID,
                        "manager_name": result.MANAGER_NAME,
                        "resource_number": result.RESOURCE_NUMBER,
                    }
                    for result in results
                ],
                "total_items": total_items,
                "page": page,
                "per_page": per_page,
                "order_by": order_by,
                "order": order,
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# This endpoint will be used for the home page dashboard section.
# This dashboard data will fetch based on filter and without filter also.
# Filtering will work on these criteria (employee id, employee name, resource name).


@home_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_home_dashboard_data():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 30))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        manager_name = request.args.get("manager_name")
        manager_id = request.args.get("manager_id")

        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            # tab_fs_emp_1 = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm_1 = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
            tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)
            tab_team_type = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)
            tab_fs_emp_upd = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD)

            # Build the query to fetch employee data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                    tab_hr_tm.EMPLOYEE_NAME.label("EMPLOYEE_NAME"),
                    tab_fs_emp.HR_STATUS.label("HR_STATUS"),
                    tab_fs_emp.MANAGER_ID.label("MANAGER_ID"),
                    tab_hr_tm_1.EMPLOYEE_NAME.label("MANAGER_NAME"),
                    tab_hr_tm.RESOURCE_NUMBER.label("RESOURCE_NUMBER"),
                    tab_fs_emp.LOCATION_CODE.label("LOCATION_CODE"),
                    tab_area.AREA_ID.label("AREA_ID"),
                    tab_area.AREA_SHORT_NAME.label("AREA_SHORT_NAME"),
                    tab_region.REGION_ID.label("REGION_ID"),
                    tab_region.REGION_NAME.label("REGION_NAME"),
                    tab_team_type.TEAM_TYPE_ID.label("TEAM_TYPE_ID"),
                    tab_team_type.TEAM_TYPE_NAME.label("TEAM_TYPE_NAME"),
                    select(func.count(tab_fs_emp_upd.CHANGE_ID))
                    .filter(tab_fs_emp_upd.EMPLOYEE_ID == tab_fs_emp.EMPLOYEE_ID)
                    .filter(tab_fs_emp_upd.CHANGE_STATUS == "Pending")
                    .label("CHANGE_COUNT"),
                    tab_fs_emp.FS_STATUS.label("FS_STATUS"),
                    tab_fs_emp.ADMIN_NOTES.label("ADMIN_NOTES"),
                )
                # .join(tab_fs_emp_1, tab_fs_emp.MANAGER_ID == tab_fs_emp_1.EMPLOYEE_ID)
                # .join(tab_hr_tm_1, tab_fs_emp_1.EMPLOYEE_ID == tab_hr_tm_1.EMPLOYEE_ID)
                .outerjoin(
                    tab_hr_tm_1, tab_fs_emp.MANAGER_ID == tab_hr_tm_1.EMPLOYEE_ID
                )
                .outerjoin(tab_area, tab_area.AREA_ID == tab_fs_emp.AREA_ID)
                .outerjoin(tab_region, tab_region.REGION_ID == tab_area.REGION_ID)
                .outerjoin(
                    tab_team_type, tab_team_type.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                # .filter(tab_fs_emp.EMPLOYEE_ID != tab_fs_emp.MANAGER_ID)
            )

            # Apply filtering based on manager_name if provided
            if manager_name:
                query = query.filter(
                    tab_hr_tm_1.EMPLOYEE_NAME.ilike(f"%{manager_name}%")
                )
            elif manager_id:
                query = query.filter(tab_fs_emp.MANAGER_ID == manager_id)
                query = query.filter(tab_fs_emp.FS_STATUS.in_(["Active", "LOA"]))

            if q:
                query = query.filter(
                    or_(
                        tab_hr_tm.RESOURCE_NUMBER.ilike(f"%{q}%"),
                        tab_hr_tm.EMPLOYEE_NAME.ilike(f"%{q}%"),
                        tab_hr_tm.EMPLOYEE_ID.ilike(f"%{q}%"),
                    )
                )
            if not manager_name and not q and not manager_id:
                query1 = session.query(tab_fs_emp.EMPLOYEE_ID)
                total_items = query1.count()
            else:
                total_items = query.count()

            # Apply sorting based on order_by and order
            query = query.order_by(
                text(order_by.upper()) if order_by and order != "desc" else None,
                text(f"{order_by.upper()} desc")
                if order_by and order == "desc"
                else None,
            )

            # Fetch the results with pagination
            results = query.offset((page - 1) * per_page).limit(per_page).all()

            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "employee_name": result.EMPLOYEE_NAME,
                        "hr_status": result.HR_STATUS,
                        "manager_id": result.MANAGER_ID,
                        "manager_name": result.MANAGER_NAME,
                        "resource_number": result.RESOURCE_NUMBER,
                        "location_code": result.LOCATION_CODE,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "change_count": result.CHANGE_COUNT,
                        "fs_status":result.FS_STATUS,
                        "admin_notes":result.ADMIN_NOTES,
                    }
                    for result in results
                ],
                "total_items": total_items,
                "page": page,
                "per_page": per_page,
                "order_by": order_by,
                "order": order,
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# This endpoint used to get data's for request changes popup screen


@home_router.route("/get_change_request", methods=["GET"])
@requestValidation.validate
def get_change_request_data_list():
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
            tab_fs_emp_upd = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD)

            # Build the query to fetch manager data
            query = (
                session.query(
                    tab_fs_emp_upd.CHANGE_ID.label("CHANGE_ID"),
                    tab_fs_emp_upd.CHANGE_EFFECTIVE_DATE,
                    tab_fs_emp_upd.CHANGE_STATUS,
                    tab_fs_emp_upd.CHANGE_NOTE,
                )
                .filter(tab_fs_emp_upd.EMPLOYEE_ID == employee_id)
                .where(tab_fs_emp_upd.CHANGE_STATUS.in_(["Pending", "Approved"]))
                .order_by(text("CHANGE_ID asc"))
                .all()
            )

            response_data = {
                "records": [
                    {
                        "change_id": result.CHANGE_ID,
                        "change_effective_date": dates.strftime(
                            result.CHANGE_EFFECTIVE_DATE, "%m-%d-%Y"
                        )
                        if result.CHANGE_EFFECTIVE_DATE
                        else None,
                        "change_status": result.CHANGE_STATUS,
                        "change_note": result.CHANGE_NOTE,
                    }
                    for result in query
                ],
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# This endpoint used to get data's for update manager popup dropdown


@home_router.route("/get_manager_list_dropdown", methods=["GET"])
@requestValidation.validate
def get_manager_list_dropdown():
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

            # Build the query to fetch manager data
            query = (
                session.query(tab_fs_emp.MANAGER_ID, tab_hr_tm.MANAGER_NAME)
                .join(tab_fs_emp, tab_fs_emp.MANAGER_ID == tab_hr_tm.EMPLOYEE_ID)
                .filter(tab_fs_emp.EMPLOYEE_ID == f"{employee_id}")
                .all()
            )

            response_data = {
                "records": [
                    {
                        "manager_id": result.MANAGER_ID,
                        "manager_name": result.MANAGER_NAME,
                    }
                    for result in query
                ],
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@home_router.route("/manager_transfer", methods=["POST"])
@requestValidation.validate
def manager_transfer():
    try:
        data_list = request.json
        affected_change_ids = []
        data = {}

        # Start a database session
        with dbSession() as session:
            current_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            current_time = datetime.utcnow().strftime("%H:%M:%S")
            for employee_id in data_list.get("employee_id"):
                # Create a new Manager Transfer record
                data["employee_id"] = employee_id
                data["manager_id"] = data_list["manager_id"]
                data["change_effective_date"] = data_list["change_effective_date"]
                data["last_edited_by"] = str(data_list["logged_in_user_id"])
                # For default value load
                data["logged_in_user_id"] = str(data_list["logged_in_user_id"])
                if "change_effective_date" in data:
                    data["change_effective_date"] += f"T{current_time}"
                # common query for emp and hr info
                tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
                tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
                # Build the query to fetch manager data
                employee_Info_query = (
                    session.query(
                        tab_fs_emp.EMPLOYEE_ID,
                        tab_fs_emp.EMPLOYEE_NAME,
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
                        tab_hr_tm.JOB_FAMILY.label("HR_JOB_FAMILY"),
                        tab_hr_tm.CONTINGENT_WORKER.label("HR_CONTINGENT_WORKER"),
                        tab_hr_tm.ACTUAL_TERMINATION_DATE.label(
                            "HR_ACTUAL_TERMINATION_DATE"
                        ),
                        tab_hr_tm.ABSENCE_START_DATE.label("HR_ABSENCE_START_DATE"),
                        tab_hr_tm.ABSENCE_END_DATE.label("HR_ABSENCE_END_DATE"),
                        tab_hr_tm.ACTUAL_RETURN_TO_WORK.label(
                            "HR_ACTUAL_RETURN_TO_WORK"
                        ),
                        tab_hr_tm.ORG_CODE.label("HR_ORG_CODE"),
                        tab_hr_tm.LAST_HIRE_DATE.label("HR_LAST_HIRE_DATE"),
                        tab_hr_tm.EBS_USER_NAME.label("HR_EBS_USER_NAME"),
                        tab_hr_tm.LAST_UPDATE_DATE.label("HR_LAST_UPDATE_DATE"),
                        tab_hr_tm.LAST_UPDATED_BY.label("HR_LAST_UPDATED_BY"),
                        tab_fs_emp.HR_STATUS.label("HR_STATUS"),
                        tab_fs_emp.OFSC_STATUS.label("OFSC_STATUS"),
                    )
                    .join(tab_hr_tm, tab_hr_tm.EMPLOYEE_ID == tab_fs_emp.EMPLOYEE_ID)
                    .filter(tab_fs_emp.EMPLOYEE_ID == employee_id)
                    .first()
                )

                if employee_Info_query:
                    service = baseService(
                        initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, session
                    )
                    # default values from fs employee table
                    tab_team_type = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)
                    team_type_Info_query = (
                        session.query(
                            tab_team_type.TEAM_TYPE_ID, tab_team_type.TEAM_TYPE_NAME
                        )
                        .filter(
                            tab_team_type.TEAM_TYPE_ID
                            == employee_Info_query.TEAM_TYPE_ID
                        )
                        .first()
                    )
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

                    data["requested_by"] = str(data_list["logged_in_user_id"])
                    data["approval_required"] = "Y"
                    data["approved"] = "N"
                    data["csa_change_comment"] = "Manager Change"
                    data["change_type"] = "UPDATE"
                    data["change_status"] = "Pending"
                    data["change_note"] = "Manager Change"
                    data["csa_notification_required"] = "Y"
                    data["last_edited_date"] = current_datetime
                    data["attribute1"] = "Manager_Transfer"
                    data["attribute2"] = str(employee_Info_query.MANAGER_ID)
                    data["employee_name"] = employee_Info_query.EMPLOYEE_NAME
                    data["hr_status"] = employee_Info_query.HR_STATUS
                    data["alternate_email"] = employee_Info_query.ALTERNATE_EMAIL
                    data["ofsc_status"] = employee_Info_query.OFSC_STATUS
                    data["alternate_email_old"] = employee_Info_query.ALTERNATE_EMAIL

                    tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
                    job_Info_query = (
                        session.query(
                            tab_job_code.JOB_ID,
                            # tab_job_code.JOB_CODE,
                            tab_job_code.JOB_TITLE,
                            tab_job_code.JOB_TYPE,
                            tab_job_code.JOB_ADP_CODE,
                        )
                        .filter(tab_job_code.JOB_ID == employee_Info_query.JOB_ID)
                        .first()
                    )

                    # data["job_code"] = (
                    #    job_Info_query.JOB_CODE if job_Info_query else None
                    # )
                    data["job_title"] = (
                        job_Info_query.JOB_TITLE if job_Info_query else None
                    )
                    data["job_adp"] = (
                        job_Info_query.JOB_ADP_CODE if job_Info_query else None
                    )
                    data["job_type"] = (
                        job_Info_query.JOB_TYPE if job_Info_query else None
                    )

                    tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
                    tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)
                    # tab_location = aliased(initialize.db_tables.RAC_FS_TM_LOC)

                    configuration_Info_query = (
                        session.query(
                            tab_area.AREA_SHORT_NAME,
                            tab_region.REGION_NAME,
                        )
                        .join(tab_region, tab_region.REGION_ID == tab_area.REGION_ID)
                        .filter(tab_area.AREA_ID == employee_Info_query.AREA_ID)
                        .first()
                    )
                    data["region"] = (
                        configuration_Info_query.REGION_NAME
                        if configuration_Info_query
                        else None
                    )
                    data["area"] = (
                        configuration_Info_query.AREA_SHORT_NAME
                        if configuration_Info_query
                        else None
                    )
                    data["loc_code"] = employee_Info_query.LOCATION_CODE

                    row = service.create(racFsTmEmployeeUpdateCreate(**data))

                    affected_change_ids.append(row.CHANGE_ID)

            response_data = {
                "records": [],
                "status": "Success",
                "message": "Manage transfer request send successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


@home_router.route("/bulk_export", methods=["POST"])
@requestValidation.validate
def bulk_export():
    try:
        data = request.json
        # Start a database session
        with dbSession() as session:
            if data["logged_in_email_id"]:
                data["lambda_status"] = "pending"
                data["email_id"] = data["logged_in_email_id"]
                service = baseService(initialize.db_tables.RAC_FS_TM_LOGS, session)
                row = service.create(racFsTmLogsCreate(**data))
                response_data = {
                    "records": [{"log_id": row.TM_LOG_ID}],
                    "status": "Success",
                    "message": "File will be shared via email. Approximate time: 15 mins",
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
        lambdaName = os.getenv("AWS_LAMBDA_EXPORT")
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


@home_router.route("/update_user_login", methods=["POST"])
@requestValidation.validate
def update_user_login():
    try:
        inp_data = request.json
        logged_in_email_id = inp_data["logged_in_email_id"]
        logged_in_user_id = inp_data["logged_in_user_id"]
        logged_in_userName = inp_data["logged_in_userName"]
        logged_in_userRole = inp_data["logged_in_userRole"]

        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_user = aliased(
                initialize.db_tables.RAC_FS_TM_USER_DETAILS, name="fs"
            )
            query = (
                session.query(tab_fs_user.EMPLOYEE_NAME).filter(
                    tab_fs_user.EMPLOYEE_ID == logged_in_user_id
                )
            ).first()
            if query:
                service = baseService(
                    initialize.db_tables.RAC_FS_TM_USER_DETAILS, session
                )
                update_query = session.query(service.model).filter(
                    service.model.EMPLOYEE_ID == logged_in_user_id
                )

                if update_query:
                    update_query.update(
                        {
                            "EMPLOYEE_NAME": logged_in_userName,
                            "EMAIL": logged_in_email_id,
                            "ROLE": logged_in_userRole,
                            "LAST_LOGIN": datetime.utcnow().strftime(
                                "%Y-%m-%dT%H:%M:%SZ"
                            ),
                        }
                    )
                    session.commit()
            else:
                insert_stmt = initialize.db_tables.RAC_FS_TM_USER_DETAILS.__table__.insert().values(
                    {
                        "EMPLOYEE_ID": logged_in_user_id,
                        "EMPLOYEE_NAME": logged_in_userName,
                        "EMAIL": logged_in_email_id,
                        "ROLE": logged_in_userRole,
                        "LAST_LOGIN": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    }
                )
                session.execute(insert_stmt)
                session.commit()

            response_data = {
                "status": "Success",
                "message": "Data retrieved successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
