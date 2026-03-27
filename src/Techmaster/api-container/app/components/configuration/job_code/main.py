import json
from datetime import date as dates
from datetime import datetime as dt

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_job_code import (
    racFsTmJobCodeCreate,
    racFsTmJobCodeUpdate,
)
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

job_code_router = Blueprint("job_code", __name__)


# Get job_code count
@job_code_router.route("/get_count", methods=["GET"])
@requestValidation.validate
def get_count():
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_JOB_CODE, session)
            job_code_count = service.get_count()
            return (
                json.loads(
                    APIResponse(
                        data={
                            "count": job_code_count,
                            "status": "Success",
                            "message": "job_code Count retrieved successfully",
                        }
                    ).to_json()
                ),
                200,
            )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get job_code details based on job_code, status and pagination
@job_code_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_job_code_pagination():
    try:
        job_adp_code = request.args.get("job_adp_code")
        status = request.args.get("status")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "last_update_date")
        order = request.args.get("order", "desc").lower()
        is_export_all = request.args.get("is_export_all", "N")

        with dbSession() as session:
            tab_job_code = aliased(initialize.db_tables.RAC_FS_TM_JOB_CODE)
            query = session.query(
                tab_job_code.JOB_ID,
                # tab_job_code.JOB_CODE,
                tab_job_code.JOB_TITLE,
                # tab_job_code.JOB_FAMILY,
                tab_job_code.JOB_TYPE,
                # tab_job_code.BUS_TYPE,
                tab_job_code.JOB_ADP_CODE,
                tab_job_code.MANAGER_FLAG,
                tab_job_code.AUTO_ADD,
                tab_job_code.APPROVAL_REQUIRED,
                tab_job_code.EFFECTIVE_START_DATE,
                tab_job_code.EFFECTIVE_END_DATE,
                tab_job_code.STATUS,
                tab_job_code.LAST_UPDATE_DATE.label("LAST_UPDATE_DATE"),
            )
            total_items = 0
            if is_export_all != "Y":
                if job_adp_code:
                    query = query.filter(
                        tab_job_code.JOB_ADP_CODE.ilike(f"%{job_adp_code}%")
                    )
                if status:
                    query = query.filter(tab_job_code.STATUS == status)
                total_items = query.count()
                query = query.order_by(
                    text(order_by.upper()) if order_by and order == "asc" else None,
                    text(f"{order_by.upper()} desc")
                    if order_by and order == "desc"
                    else None,
                )
                results = query.offset((page - 1) * per_page).limit(per_page).all()
            else:
                if status:
                    query = query.filter(tab_job_code.STATUS == status)
                query = query.order_by(
                    text(order_by.upper()) if order_by and order == "asc" else None,
                    text(f"{order_by.upper()} desc")
                    if order_by and order == "desc"
                    else None,
                )
                total_items = query.count()
                results = query.all()

            if results:
                response_data = {
                    "records": [
                        {
                            "job_id": result.JOB_ID,
                            # "job_code": result.JOB_CODE,
                            "job_title": result.JOB_TITLE,
                            # "job_family": result.JOB_FAMILY,
                            "job_type": result.JOB_TYPE,
                            # "bus_type": result.BUS_TYPE,
                            "job_adp_code": result.JOB_ADP_CODE,
                            "manager_flag": result.MANAGER_FLAG,
                            "auto_add": result.AUTO_ADD,
                            "approval_required": result.APPROVAL_REQUIRED,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
                            "status": result.STATUS,
                            "status": result.STATUS,
                        }
                        for result in results
                    ],
                    "total_items": total_items,
                    "page": page,
                    "per_page": per_page,
                    "order_by": order_by,
                    "order": order,
                    "status": "Success",
                    "message": "job_code retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "job_code not found"}]
                response_data = {"records": [], "total_items": 0}
                return (
                    json.loads(
                        APIResponse(data=response_data, errors=error_response).to_json()
                    ),
                    200,
                )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get job_code details based on job_code id
@job_code_router.route("/get/<int:job_id>", methods=["GET"])
@requestValidation.validate
def get_job_code_by_id(job_id: int):
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_JOB_CODE, session)
            result = service.get_pk_id(job_id)
            if result:
                response_data = {
                    "records": [
                        {
                            "job_id": result.JOB_ID,
                            # "job_code": result.JOB_CODE,
                            "job_title": result.JOB_TITLE,
                            # "job_family": result.JOB_FAMILY,
                            "job_type": result.JOB_TYPE,
                            # "bus_type": result.BUS_TYPE,
                            "job_adp_code": result.JOB_ADP_CODE,
                            "manager_flag": result.MANAGER_FLAG,
                            "auto_add": result.AUTO_ADD,
                            "approval_required": result.APPROVAL_REQUIRED,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
                            "status": result.STATUS,
                            "status": result.STATUS,
                        }
                    ],
                    "status": "Success",
                    "message": "job_code retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "job_code not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Create new job_code
@job_code_router.route("/add", methods=["POST"])
@requestValidation.validate
def add_job_code():
    try:
        data = request.json

        with dbSession() as session:
            if "effective_start_date" in data:
                current_time = dt.utcnow().strftime("%H:%M:%S")
                data["effective_start_date"] += f"T{current_time}"
                service = baseService(initialize.db_tables.RAC_FS_TM_JOB_CODE, session)
                row = service.create(racFsTmJobCodeCreate(**data))
                response_data = {
                    "records": [{"job_id": row.JOB_ID}],
                    "status": "Success",
                    "message": "job_code created successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 201
            else:
                response_data = {
                    "status": "Failed",
                    "message": "effective_start_date is mandatory",
                }
                return json.loads(APIResponse(errors=response_data).to_json()), 400

    except IntegrityError as e:
        error_response = [
            {
                "status": "Failed",
                "message": "Job ADP Code already exists in our record.",
            }
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Update existing job_code
@job_code_router.route("/update/<int:job_id>", methods=["PUT"])
@requestValidation.validate
def update_job_code(job_id: int):
    try:
        data = request.json
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_JOB_CODE, session)
            job_code_row = service.get_pk_id(job_id)
            if job_code_row:
                if "effective_start_date" in data:
                    current_time = dt.utcnow().strftime("%H:%M:%S")
                    data["effective_start_date"] += f"T{current_time}"
                else:
                    data["effective_start_date"] = job_code_row.EFFECTIVE_START_DATE

                if data["status"] == "INACTIVE":
                    current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    data["effective_end_date"] = current_datetime_utc
                else:
                    data["effective_end_date"] = None

                row = service.update(job_code_row, racFsTmJobCodeUpdate(**data))
                response_data = {
                    "records": [{"job_id": row.JOB_ID}],
                    "status": "Success",
                    "message": "job_code updated successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "job_code not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except IntegrityError as e:
        error_response = [
            {
                "status": "Failed",
                "message": "Job ADP Code already exists in our record.",
            }
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Bulk Delete
@job_code_router.route("/update/bulk-delete", methods=["PUT"])
@requestValidation.validate
def bulk_delete():
    try:
        data = request.json
        if "job_id" not in data or "logged_in_user_id" not in data:
            error_response = [
                {
                    "status": "Failed",
                    "message": "Missing required fields 'job_id' or 'logged_in_user_id'.",
                }
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        job_ids = data["job_id"]
        logged_in_user_id = data["logged_in_user_id"]

        if not job_ids:
            error_response = [
                {"status": "Failed", "message": "job_id list cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_JOB_CODE, session)
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            for job_id in job_ids:
                session.query(service.model).filter(
                    service.model.JOB_ID == job_id
                ).update(
                    {
                        "STATUS": "INACTIVE",
                        "EFFECTIVE_END_DATE": current_datetime_utc,
                        "LAST_UPDATED_BY": logged_in_user_id,
                    },
                    synchronize_session=False,
                )

            # Commit the changes to the database
            session.commit()

            response_data = {
                "records": [{"job_id": job_ids}],
                "status": "Success",
                "message": "Job(s) deactivated successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
