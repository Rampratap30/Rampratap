import json
from datetime import date as dates
from datetime import datetime as dt

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_region import (
    racFsTmRegionCreate,
    racFsTmRegionUpdate,
)
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

region_router = Blueprint("region", __name__)


# Get Region count
@region_router.route("/get_count", methods=["GET"])
@requestValidation.validate
def get_count():
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_REGION, session)
            region_count = service.get_count()
            return (
                json.loads(
                    APIResponse(
                        data={
                            "count": region_count,
                            "status": "Success",
                            "message": "Region Count retrieved successfully",
                        }
                    ).to_json()
                ),
                200,
            )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get Region details based on region, status and pagination
@region_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_region_pagination():
    try:
        region_name = request.args.get("region_name")
        status = request.args.get("status")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "last_update_date")
        order = request.args.get("order", "desc").lower()
        is_export_all = request.args.get("is_export_all", "N")

        with dbSession() as session:
            tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            query = session.query(
                tab_region.REGION_ID,
                tab_region.REGION_NAME,
                tab_region.REGION_SHORT_NAME,
                tab_region.REGION_DIR_EMP_ID,
                tab_region.EFFECTIVE_START_DATE,
                tab_region.EFFECTIVE_END_DATE,
                tab_region.STATUS,
                tab_hr_tm.RESOURCE_NUMBER,
                tab_hr_tm.EMPLOYEE_NAME,
                tab_hr_tm.EMAIL,
                tab_region.LAST_UPDATE_DATE.label("LAST_UPDATE_DATE"),
            ).filter(tab_hr_tm.EMPLOYEE_ID == tab_region.REGION_DIR_EMP_ID)
            total_items = 0
            if is_export_all != "Y":
                if region_name:
                    query = query.filter(
                        tab_region.REGION_NAME.ilike(f"%{region_name}%")
                    )
                if status:
                    query = query.filter(tab_region.STATUS == status)

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
                    query = query.filter(tab_region.STATUS == status)
                total_items = query.count()
                results = query.all()

            if results:
                response_data = {
                    "records": [
                        {
                            "region_id": result.REGION_ID,
                            "region_name": result.REGION_NAME,
                            "region_short_name": result.REGION_SHORT_NAME,
                            "region_dir_emp_id": result.REGION_DIR_EMP_ID,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
                            "status": result.STATUS,
                            "dir_resource_number": result.RESOURCE_NUMBER,
                            "dir_employee_name": result.EMPLOYEE_NAME,
                            "dir_email": result.EMAIL,
                        }
                        for result in results
                    ],
                    "total_items": total_items,
                    "page": page,
                    "per_page": per_page,
                    "order_by": order_by,
                    "order": order,
                    "status": "Success",
                    "message": "Region retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Region not found"}]
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


# Get Region details based on Region id
@region_router.route("/get/<int:region_id>", methods=["GET"])
@requestValidation.validate
def get_region_by_id(region_id: int):
    try:
        with dbSession() as session:
            tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            results = (
                session.query(
                    tab_region.REGION_ID,
                    tab_region.REGION_NAME,
                    tab_region.REGION_SHORT_NAME,
                    tab_region.REGION_DIR_EMP_ID,
                    tab_region.EFFECTIVE_START_DATE,
                    tab_region.EFFECTIVE_END_DATE,
                    tab_region.STATUS,
                    tab_hr_tm.RESOURCE_NUMBER,
                    tab_hr_tm.EMPLOYEE_NAME,
                    tab_hr_tm.EMAIL,
                )
                .filter(tab_hr_tm.EMPLOYEE_ID == tab_region.REGION_DIR_EMP_ID)
                .filter(tab_region.REGION_ID == region_id)
                .all()
            )
            if results:
                response_data = {
                    "records": [
                        {
                            "region_id": result.REGION_ID,
                            "region_name": result.REGION_NAME,
                            "region_short_name": result.REGION_SHORT_NAME,
                            "region_dir_emp_id": result.REGION_DIR_EMP_ID,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
                            "status": result.STATUS,
                            "dir_resource_number": result.RESOURCE_NUMBER,
                            "dir_employee_name": result.EMPLOYEE_NAME,
                            "dir_email": result.EMAIL,
                        }
                        for result in results
                    ],
                    "status": "Success",
                    "message": "Region retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Region not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Create new region
@region_router.route("/add", methods=["POST"])
@requestValidation.validate
def add_region():
    try:
        data = request.json

        with dbSession() as session:
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            dir_validation = (
                session.query(tab_hr_tm)
                .filter(tab_hr_tm.EMPLOYEE_ID == data["region_dir_emp_id"])
                .all()
            )
            if not dir_validation:
                error_response = [
                    {"status": "Failed", "message": "Invalid region_dir_emp_id"}
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 400

            if "effective_start_date" in data:
                current_time = dt.utcnow().strftime("%H:%M:%S")
                data["effective_start_date"] += f"T{current_time}"
                service = baseService(initialize.db_tables.RAC_FS_TM_REGION, session)
                row = service.create(racFsTmRegionCreate(**data))
                response_data = {
                    "records": [{"region_id": row.REGION_ID}],
                    "status": "Success",
                    "message": "Region created successfully",
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
            {"status": "Failed", "message": "Region already exists in our record."}
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Update existing Region
@region_router.route("/update/<int:region_id>", methods=["PUT"])
@requestValidation.validate
def update_region(region_id: int):
    try:
        data = request.json
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_REGION, session)
            region = service.get_pk_id(region_id)
            if region:
                if data.get("region_dir_emp_id"):
                    tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
                    dir_validation = (
                        session.query(tab_hr_tm)
                        .filter(tab_hr_tm.EMPLOYEE_ID == data["region_dir_emp_id"])
                        .all()
                    )
                    if not dir_validation:
                        error_response = [
                            {"status": "Failed", "message": "Invalid region_dir_emp_id"}
                        ]
                        return (
                            json.loads(APIResponse(errors=error_response).to_json()),
                            400,
                        )
                if "effective_start_date" in data:
                    current_time = dt.utcnow().strftime("%H:%M:%S")
                    data["effective_start_date"] += f"T{current_time}"
                else:
                    data["effective_start_date"] = region.EFFECTIVE_START_DATE

                if data["status"] == "INACTIVE":
                    current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    data["effective_end_date"] = current_datetime_utc
                else:
                    data["effective_end_date"] = None

                region_update = service.update(region, racFsTmRegionUpdate(**data))
                response_data = {
                    "records": [{"region_id": region_update.REGION_ID}],
                    "status": "Success",
                    "message": "Region updated successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Region not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except IntegrityError as e:
        error_response = [
            {"status": "Failed", "message": "Region already exists in our record."}
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Bulk Delete
@region_router.route("/update/bulk-delete", methods=["PUT"])
@requestValidation.validate
def bulk_delete():
    try:
        data = request.json
        if "region_id" not in data or "logged_in_user_id" not in data:
            error_response = [
                {
                    "status": "Failed",
                    "message": "Missing required fields 'region_id' or 'logged_in_user_id'.",
                }
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        region_ids = data["region_id"]
        logged_in_user_id = data["logged_in_user_id"]

        if not region_ids:
            error_response = [
                {"status": "Failed", "message": "region_id list cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_REGION, session)
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            for region_id in region_ids:
                session.query(service.model).filter(
                    service.model.REGION_ID == region_id
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
                "records": [{"region_id": region_ids}],
                "status": "Success",
                "message": "Region(s) deactivated successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
