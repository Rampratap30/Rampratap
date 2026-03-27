import json
from datetime import date as dates
from datetime import datetime, timedelta
from collections import OrderedDict

from flask import Blueprint, request
from sqlalchemy import desc, func, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

view_router = Blueprint("view", __name__)


# This endpoint will be used for the home page filter section.
# It can be used in the new hire records.
@view_router.route("/get_new_hire_list", methods=["GET"])
@requestValidation.validate
def get_new_hire_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        is_export_all = request.args.get("is_export_all", "N")

        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_area.AREA_ID == tab_fs_emp.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_job.JOB_ID == tab_fs_emp.JOB_ID)
                .filter(tab_fs_emp.CREATION_DATE >= datetime.now() - timedelta(days=30))
            )

            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )
                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()

            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the recent term records.
@view_router.route("/get_recent_term_list", methods=["GET"])
@requestValidation.validate
def get_recent_term_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        is_export_all = request.args.get("is_export_all", "N")
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        # Start a database session
        with dbSession() as session:
            current_date = datetime.now()
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                    tab_hr_tm.HR_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(
                    tab_hr_tm.ACTUAL_TERMINATION_DATE
                    > current_date - timedelta(days=30)
                )
            )
            # HR Status
            if empStatus == "Active":
                query = query.filter(tab_hr_tm.HR_STATUS == "Active")
            elif empStatus:
                query = query.filter(tab_hr_tm.HR_STATUS != "Active")
            # FS Status
            if fsStatus:
                query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))
            # Job Type
            if jobType:
                query = query.filter(tab_job.JOB_TYPE == jobType)

            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                total_items = query.count()
                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the hierarchy mismatches records.
@view_router.route("/get_hierarchy_mismatches_list", methods=["GET"])
@requestValidation.validate
def get_hierarchy_mismatches_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_fs_emp_m = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="tab_fs_emp_m"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_hr_tm_m = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="tab_hr_tm_m"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_reg_m = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="tab_reg_m")
            tab_area_m = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="tab_area_m")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_hr_tm_m.EMPLOYEE_NAME.label("MANAGER_NAME"),
                    tab_reg_m.REGION_NAME.label("M_REGION"),
                    tab_area_m.AREA_ID.label("M_AREA_ID"),
                    tab_area_m.AREA_SHORT_NAME.label("M_AREA_SHORT_NAME"),
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_area.AREA_ID == tab_fs_emp.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .join(tab_fs_emp_m, tab_fs_emp_m.EMPLOYEE_ID == tab_fs_emp.MANAGER_ID)
                .join(tab_hr_tm_m, tab_fs_emp_m.EMPLOYEE_ID == tab_hr_tm_m.EMPLOYEE_ID)
                .join(tab_area_m, tab_area_m.AREA_ID == tab_fs_emp_m.AREA_ID)
                .join(tab_reg_m, tab_reg_m.REGION_ID == tab_area_m.REGION_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(
                    or_(
                        # func.upper(tab_fs_emp.LOCATION_CODE)
                        #!= func.upper(tab_hr_tm.LOCATION_CODE),
                        func.upper(tab_area_m.AREA_SHORT_NAME)
                        != func.upper(tab_area.AREA_SHORT_NAME),
                        func.upper(tab_reg.REGION_NAME)
                        != func.upper(tab_reg_m.REGION_NAME),
                    )
                )
            )
            total_items = 0
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        # "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "system_area_short_name": result.M_AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "system_region_name": result.M_REGION,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the job mismatches records.
@view_router.route("/get_job_mismatches_list", methods=["GET"])
@requestValidation.validate
def get_job_mismatches_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)

        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_hr_tm.JOB_ADP.label("HR_JOB_ADP"),
                    tab_job.JOB_ADP_CODE,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(
                    func.upper(tab_hr_tm.JOB_ADP) != func.upper(tab_job.JOB_ADP_CODE)
                )
            )
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        # "team_type_name": result.TEAM_TYPE_NAME,
                        # "area_short_name": result.AREA_SHORT_NAME,
                        # "region_name": result.REGION_NAME,
                        "job_adp": result.JOB_ADP_CODE,
                        "system_job_adp": result.HR_JOB_ADP,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the manager mismatches records.
@view_router.route("/get_manager_mismatches_list", methods=["GET"])
@requestValidation.validate
def get_manager_mismatches_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_hr_mgr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrMgrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME.label("HR_MANAGER_NAME"),
                    tab_hr_mgr_tm.EMPLOYEE_NAME.label("MANAGER_NAME"),
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_hr_mgr_tm, tab_fs_emp.MANAGER_ID == tab_hr_mgr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(
                    func.upper(tab_hr_tm.MANAGER_EMPLOYEE_ID)
                    != func.upper(tab_fs_emp.MANAGER_ID)
                )
            )
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "system_manager_name": result.HR_MANAGER_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        # "team_type_name": result.TEAM_TYPE_NAME,
                        # "area_short_name": result.AREA_SHORT_NAME,
                        # "region_name": result.REGION_NAME,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the all mismatches records.
@view_router.route("/get_all_mismatches_list", methods=["GET"])
@requestValidation.validate
def get_all_mismatches_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(
                    or_(
                        # func.upper(tab_fs_emp.LOCATION_CODE)
                        #!= func.upper(tab_hr_tm.LOCATION_CODE),
                        func.upper(tab_reg.REGION_NAME) != func.upper(tab_hr_tm.REGION),
                        func.upper(tab_hr_tm.JOB_ADP)
                        != func.upper(tab_job.JOB_ADP_CODE),
                        func.upper(tab_hr_tm.MANAGER_EMPLOYEE_ID)
                        != func.upper(tab_fs_emp.MANAGER_ID),
                        func.upper(tab_hr_tm.AREA_SHORT)
                        != func.upper(tab_area.AREA_SHORT_NAME),
                    )
                )
            )
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the record not complete records.
@view_router.route("/get_record_not_complete_list", methods=["GET"])
@requestValidation.validate
def get_record_not_complete_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(func.upper(tab_fs_emp.RECORD_COMPLETE) == "N")
            )
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()

            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the admin review records.
@view_router.route("/get_admin_review_list", methods=["GET"])
@requestValidation.validate
def get_admin_review_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)

        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_emp_upd = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_UPD, name="upd"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_emp_upd,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .join(tab_emp_upd, tab_fs_emp.EMPLOYEE_ID == tab_emp_upd.EMPLOYEE_ID)
                .filter(tab_emp_upd.REVIEW_DATE != "NULL")
            )
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the admin review records.
@view_router.route("/get_managers_not_self_list", methods=["GET"])
@requestValidation.validate
def get_managers_not_self_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(tab_fs_emp.MANAGER_FLAG == "Y")
                .filter(tab_fs_emp.MANAGER_ID != tab_fs_emp.EMPLOYEE_ID)
            )
            total_items = 0
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
# It can be used in the admin review records.
@view_router.route("/get_loa_list", methods=["GET"])
@requestValidation.validate
def get_loa_list():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", None)
        order = request.args.get("order", "asc").lower()
        q = request.args.get("q", None)
        empStatus = request.args.get("status", None)
        fsStatus = request.args.get("fs_status", None)
        jobType = request.args.get("job_type", None)
        is_export_all = request.args.get("is_export_all", "N")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(
                initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS, name="emp"
            )
            tab_hr_tm = aliased(
                initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS, name="hrEmp"
            )
            tab_reg = aliased(initialize.db_tables.RAC_FS_TM_REGION, name="reg")
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA, name="area")
            tab_team = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, name="tm")
            tab_job = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE, name="job")

            # Build the query to fetch data
            query = (
                session.query(
                    tab_fs_emp.EMPLOYEE_ID,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.MANAGER_NAME,
                    tab_hr_tm.AREA,
                    tab_hr_tm.HR_STATUS,
                    tab_reg.REGION_NAME,
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_team.TEAM_TYPE_NAME,
                    tab_job.JOB_ID,
                    tab_fs_emp.ADMIN_NOTES,
                    tab_fs_emp.FS_STATUS,
                )
                .join(tab_hr_tm, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_area, tab_fs_emp.AREA_ID == tab_area.AREA_ID)
                .join(tab_reg, tab_reg.REGION_ID == tab_area.REGION_ID)
                .outerjoin(tab_team, tab_team.TEAM_TYPE_ID == tab_fs_emp.TEAM_TYPE_ID)
                .join(tab_job, tab_fs_emp.JOB_ID == tab_job.JOB_ID)
                .filter(func.upper(tab_hr_tm.HR_STATUS).like("%LOA%"))
            )
            total_items = 0
            if is_export_all != "Y":
                if q:
                    query = query.filter(
                        or_(
                            tab_hr_tm.RESOURCE_NUMBER.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_NAME.like(f"%{q}%"),
                            tab_hr_tm.EMPLOYEE_ID.like(f"%{q}%"),
                        )
                    )

                # HR Status
                if empStatus == "Active":
                    query = query.filter(tab_hr_tm.HR_STATUS == "Active")
                elif empStatus:
                    query = query.filter(tab_hr_tm.HR_STATUS != "Active")

                # FS Status
                if fsStatus:
                    query = query.filter(tab_fs_emp.FS_STATUS.ilike(f"{fsStatus}"))

                # Job Type
                if jobType:
                    query = query.filter(tab_job.JOB_TYPE == jobType)

                total_items = query.count()

                # Apply sorting based on order_by and order
                query = query.order_by(
                    text(order_by) if order_by else None,
                    text(f"{order_by} desc") if order_by and order == "desc" else None,
                )
                # Fetch the results with pagination
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                total_items = query.count()
                results = query.all()
            response_data = {
                "records": [
                    {
                        "employee_id": result.EMPLOYEE_ID,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "manager_name": result.MANAGER_NAME,
                        "team_type_name": result.TEAM_TYPE_NAME,
                        "area_short_name": result.AREA_SHORT_NAME,
                        "region_name": result.REGION_NAME,
                        "admin_notes": result.ADMIN_NOTES,
                        "hr_status": result.HR_STATUS,
                        "fs_status": result.FS_STATUS,
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
