import json

from flask import Blueprint, request
from sqlalchemy import desc, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

common_router = Blueprint("common", __name__)

# This endpoint will be used for the add region popup section.
# It can be used to fetch dir list.


@common_router.route("/dir-list", methods=["GET"])
@requestValidation.validate
def get_dir_list():
    try:
        # Extract query parameters from the request
        dir_id = request.args.get("dir_id")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
            DIR_TYPE = "DIR"
            # Build the query to fetch manager data
            query = (
                session.query(
                    tab_hr_tm.EMAIL,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.EMPLOYEE_ID,
                )
                .join(tab_fs_emp, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_job_code, tab_job_code.JOB_ID == tab_fs_emp.JOB_ID)
                .filter(tab_job_code.JOB_TYPE.like(f"%{DIR_TYPE}%"))
            )

            # Apply filtering based on dir_id if provided
            if dir_id:
                query = query.filter(tab_hr_tm.EMPLOYEE_ID.like(f"%{dir_id}%"))

            response_data = {
                "records": [
                    {
                        "email": result.EMAIL,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "employee_id": result.EMPLOYEE_ID,
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


# This endpoint will be used for the add area popup section.
# It can be used to fetch dir list.


@common_router.route("/fom-list", methods=["GET"])
@requestValidation.validate
def get_fom_list():
    try:
        # Extract query parameters from the request
        dir_id = request.args.get("dir_id")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_fs_emp = aliased(initialize.db_tables.RAC_FS_TM_EMPLOYEE_DTLS)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
            FOM_TYPE = "OPS"
            # Build the query to fetch manager data
            query = (
                session.query(
                    tab_hr_tm.EMAIL,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.EMPLOYEE_ID,
                )
                .join(tab_fs_emp, tab_fs_emp.EMPLOYEE_ID == tab_hr_tm.EMPLOYEE_ID)
                .join(tab_job_code, tab_job_code.JOB_ID == tab_fs_emp.JOB_ID)
                .filter(tab_job_code.JOB_TYPE.like(f"%{FOM_TYPE}%"))
            )

            # Apply filtering based on dir_id if provided
            if dir_id:
                query = query.filter(tab_hr_tm.EMPLOYEE_ID.like(f"%{dir_id}%"))

            response_data = {
                "records": [
                    {
                        "email": result.EMAIL,
                        "resource_number": result.RESOURCE_NUMBER,
                        "employee_name": result.EMPLOYEE_NAME,
                        "employee_id": result.EMPLOYEE_ID,
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


@common_router.route("/area-fom", methods=["GET"])
@requestValidation.validate
def get_area_fom_list():
    try:
        # Extract query parameters from the request
        area = request.args.get("area")
        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            # Build the query to fetch manager data
            query = (
                session.query(
                    tab_hr_tm.EMPLOYEE_NAME.label("EMPLOYEE_NAME"),
                    tab_hr_tm.RESOURCE_NUMBER.label("RESOURCE_NUMBER"),
                    tab_hr_tm.EMPLOYEE_ID.label("EMPLOYEE_ID"),
                )
                .join(tab_area, tab_area.AREA_FOM_EMP_ID == tab_hr_tm.EMPLOYEE_ID)
                .filter(tab_area.AREA_SHORT_NAME.ilike(f"%{area}%"))
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
                "page": None,
                "per_page": None,
                "order_by": None,
                "order": None,
                "status": "Success",
                "message": "Data retrieved successfully",
            }

            return json.loads(APIResponse(data=response_data).to_json()), 200

    except Exception as e:
        # Handle exceptions and return a 500 error response
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
