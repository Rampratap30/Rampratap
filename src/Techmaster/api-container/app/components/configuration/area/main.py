import json
from datetime import date as dates
from datetime import datetime as dt

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_area import racFsTmAreaCreate, racFsTmAreaUpdate
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

area_router = Blueprint("area", __name__)


# Get AREA count
@area_router.route("/get_count", methods=["GET"])
@requestValidation.validate
def get_count():
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_AREA, session)
            area_count = service.get_count()
            return (
                json.loads(
                    APIResponse(
                        data={
                            "count": area_count,
                            "status": "Success",
                            "message": "Area Count retrieved successfully",
                        }
                    ).to_json()
                ),
                200,
            )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get AREA details based on AREA, status and pagination
@area_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_area_pagination():
    try:
        area_short_name = request.args.get("area_short_name")
        status = request.args.get("status")
        region_name = request.args.get("region_name")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "last_update_date")
        order = request.args.get("order", "desc").lower()
        is_export_all = request.args.get("is_export_all", "N")

        with dbSession() as session:
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
            tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)
            tab_dir_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_fom_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            query = (
                session.query(
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_area.REGION_ID,
                    tab_region.REGION_NAME,
                    tab_area.AREA_DIR_EMP_ID,
                    tab_area.AREA_FOM_EMP_ID,
                    tab_area.EFFECTIVE_START_DATE,
                    tab_area.EFFECTIVE_END_DATE,
                    tab_area.STATUS,
                    tab_dir_hr_tm.RESOURCE_NUMBER.label("DIR_RESOURCE_NUMBER"),
                    tab_dir_hr_tm.EMPLOYEE_NAME.label("DIR_NAME"),
                    tab_fom_hr_tm.RESOURCE_NUMBER.label("FOM_RESOURCE_NUMBER"),
                    tab_fom_hr_tm.EMPLOYEE_NAME.label("FOM_NAME"),
                    tab_area.LAST_UPDATE_DATE.label("LAST_UPDATE_DATE"),
                )
                .outerjoin(
                    tab_dir_hr_tm, tab_dir_hr_tm.EMPLOYEE_ID == tab_area.AREA_DIR_EMP_ID
                )
                .outerjoin(
                    tab_fom_hr_tm, tab_fom_hr_tm.EMPLOYEE_ID == tab_area.AREA_FOM_EMP_ID
                )
                .outerjoin(tab_region, tab_region.REGION_ID == tab_area.REGION_ID)
            )
            total_items = 0
            if is_export_all != "Y":
                if area_short_name:
                    query = query.filter(
                        tab_area.AREA_SHORT_NAME.ilike(f"%{area_short_name}%")
                    )
                if status:
                    query = query.filter(tab_area.STATUS == status)
                if region_name:
                    query = query.filter(tab_region.REGION_NAME == region_name)
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
                    query = query.filter(tab_area.STATUS == status)
                if region_name:
                    query = query.filter(tab_region.REGION_NAME == region_name)
                total_items = query.count()
                results = query.all()

            if results:
                response_data = {
                    "records": [
                        {
                            "area_id": result.AREA_ID,
                            "area_short_name": result.AREA_SHORT_NAME,
                            "region_id": result.REGION_ID,
                            "region_name": result.REGION_NAME,
                            "area_dir_emp_id": result.AREA_DIR_EMP_ID,
                            "area_fom_emp_id": result.AREA_FOM_EMP_ID,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
                            "status": result.STATUS,
                            "dir_resource_number": result.DIR_RESOURCE_NUMBER,
                            "dir_employee_name": result.DIR_NAME,
                            "fom_resource_number": result.FOM_RESOURCE_NUMBER,
                            "fom_employee_name": result.FOM_NAME,
                        }
                        for result in results
                    ],
                    "total_items": total_items,
                    "page": page,
                    "per_page": per_page,
                    "order_by": order_by,
                    "order": order,
                    "status": "Success",
                    "message": "Area retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Area not found"}]
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


# Get AREA details based on AREA id
@area_router.route("/get/<int:area_id>", methods=["GET"])
@requestValidation.validate
def get_area_by_id(area_id: int):
    try:
        with dbSession() as session:
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
            tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)
            tab_dir_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            tab_fom_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            results = (
                session.query(
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                    tab_area.REGION_ID,
                    tab_region.REGION_NAME,
                    tab_area.AREA_DIR_EMP_ID,
                    tab_area.AREA_FOM_EMP_ID,
                    tab_area.EFFECTIVE_START_DATE,
                    tab_area.EFFECTIVE_END_DATE,
                    tab_area.STATUS,
                    tab_dir_hr_tm.RESOURCE_NUMBER.label("DIR_RESOURCE_NUMBER"),
                    tab_dir_hr_tm.EMPLOYEE_NAME.label("DIR_NAME"),
                    tab_fom_hr_tm.RESOURCE_NUMBER.label("FOM_RESOURCE_NUMBER"),
                    tab_fom_hr_tm.EMPLOYEE_NAME.label("FOM_NAME"),
                )
                .outerjoin(
                    tab_dir_hr_tm, tab_dir_hr_tm.EMPLOYEE_ID == tab_area.AREA_DIR_EMP_ID
                )
                .outerjoin(
                    tab_fom_hr_tm, tab_fom_hr_tm.EMPLOYEE_ID == tab_area.AREA_FOM_EMP_ID
                )
                .outerjoin(tab_region, tab_region.REGION_ID == tab_area.REGION_ID)
                .filter(tab_area.AREA_ID == area_id)
                .all()
            )

            if results:
                response_data = {
                    "records": [
                        {
                            "area_id": result.AREA_ID,
                            "area_short_name": result.AREA_SHORT_NAME,
                            "region_id": result.REGION_ID,
                            "region_name": result.REGION_NAME,
                            "area_dir_emp_id": result.AREA_DIR_EMP_ID,
                            "area_fom_emp_id": result.AREA_FOM_EMP_ID,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
                            "status": result.STATUS,
                            "dir_resource_number": result.DIR_RESOURCE_NUMBER,
                            "dir_employee_name": result.DIR_NAME,
                            "fom_resource_number": result.FOM_RESOURCE_NUMBER,
                            "fom_employee_name": result.FOM_NAME,
                        }
                        for result in results
                    ],
                    "status": "Success",
                    "message": "Area retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Area not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Create new Area
@area_router.route("/add", methods=["POST"])
@requestValidation.validate
def add_area():
    try:
        data = request.json

        with dbSession() as session:
            tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
            dir_validation = (
                session.query(tab_hr_tm)
                .filter(tab_hr_tm.EMPLOYEE_ID == data["area_dir_emp_id"])
                .all()
            )

            if not dir_validation:
                error_response = [
                    {"status": "Failed", "message": "Invalid area_dir_emp_id"}
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 400

            fom_validation = (
                session.query(tab_hr_tm)
                .filter(tab_hr_tm.EMPLOYEE_ID == data["area_fom_emp_id"])
                .all()
            )
            if not fom_validation:
                error_response = [
                    {"status": "Failed", "message": "Invalid area_fom_emp_id"}
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 400

            tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)

            region_validation = (
                session.query(tab_region)
                .filter(tab_region.REGION_ID == data["region_id"])
                .all()
            )
            if not region_validation:
                error_response = [{"status": "Failed", "message": "Invalid region_id"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 400

            if "effective_start_date" in data:
                current_time = dt.utcnow().strftime("%H:%M:%S")
                data["effective_start_date"] += f"T{current_time}"
                service = baseService(initialize.db_tables.RAC_FS_TM_AREA, session)
                row = service.create(racFsTmAreaCreate(**data))
                response_data = {
                    "records": [{"area_id": row.AREA_ID}],
                    "status": "Success",
                    "message": "Area created successfully",
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
            {"status": "Failed", "message": "Area already exists in our record."}
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Update existing area
@area_router.route("/update/<int:area_id>", methods=["PUT"])
@requestValidation.validate
def update_area(area_id: int):
    try:
        data = request.json
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_AREA, session)
            AREA = service.get_pk_id(area_id)
            if AREA:
                if data.get("area_dir_emp_id"):
                    tab_hr_tm = aliased(initialize.db_tables.RAC_HR_TM_EMPLOYEE_DTLS)
                    tab_region = aliased(initialize.db_tables.RAC_FS_TM_REGION)
                    dir_validation = (
                        session.query(tab_hr_tm)
                        .filter(tab_hr_tm.EMPLOYEE_ID == data["area_dir_emp_id"])
                        .all()
                    )

                    if not dir_validation:
                        error_response = [
                            {"status": "Failed", "message": "Invalid area_dir_emp_id"}
                        ]
                        return (
                            json.loads(APIResponse(data=error_response).to_json()),
                            400,
                        )

                    fom_validation = (
                        session.query(tab_hr_tm)
                        .filter(tab_hr_tm.EMPLOYEE_ID == data["area_fom_emp_id"])
                        .all()
                    )
                    if not fom_validation:
                        error_response = [
                            {"status": "Failed", "message": "Invalid area_fom_emp_id"}
                        ]
                        return (
                            json.loads(APIResponse(errors=error_response).to_json()),
                            400,
                        )

                    region_validation = (
                        session.query(tab_region)
                        .filter(tab_region.REGION_ID == data["region_id"])
                        .all()
                    )
                    if not region_validation:
                        error_response = [
                            {"status": "Failed", "message": "Invalid region_id"}
                        ]
                        return (
                            json.loads(APIResponse(errors=error_response).to_json()),
                            400,
                        )
                if "effective_start_date" in data:
                    current_time = dt.utcnow().strftime("%H:%M:%S")
                    data["effective_start_date"] += f"T{current_time}"
                else:
                    data["effective_start_date"] = AREA.EFFECTIVE_START_DATE

                if data["status"] == "INACTIVE":
                    current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    data["effective_end_date"] = current_datetime_utc
                else:
                    data["effective_end_date"] = None

                row = service.update(AREA, racFsTmAreaUpdate(**data))
                response_data = {
                    "records": [{"area_id": row.AREA_ID}],
                    "status": "Success",
                    "message": "Area updated successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "area not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except IntegrityError as e:
        error_response = [
            {"status": "Failed", "message": "Area already exists in our record."}
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Bulk Delete
@area_router.route("/update/bulk-delete", methods=["PUT"])
@requestValidation.validate
def bulk_delete():
    try:
        data = request.json
        if "area_id" not in data or "logged_in_user_id" not in data:
            error_response = [
                {
                    "status": "Failed",
                    "message": "Missing required fields 'area_id' or 'logged_in_user_id'.",
                }
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        area_ids = data["area_id"]
        logged_in_user_id = data["logged_in_user_id"]

        if not area_ids:
            error_response = [
                {"status": "Failed", "message": "area_id list cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_AREA, session)
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            for area_id in area_ids:
                session.query(service.model).filter(
                    service.model.AREA_ID == area_id
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
                "records": [{"area_id": area_ids}],
                "status": "Success",
                "message": "Region(s) deactivated successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get AREA details based on REGION_ID
@area_router.route("/get_area_list/<int:region_id>", methods=["GET"])
@requestValidation.validate
def get_area_list(region_id: int):
    try:
        with dbSession() as session:
            tab_area = aliased(initialize.db_tables.RAC_FS_TM_AREA)
            query = (
                session.query(
                    tab_area.AREA_ID,
                    tab_area.AREA_SHORT_NAME,
                )
                .filter(tab_area.REGION_ID == region_id)
                .all()
            )
            if query:
                response_data = {
                    "records": [
                        {
                            "area_id": result.AREA_ID,
                            "area_short_name": result.AREA_SHORT_NAME,
                        }
                        for result in query
                    ],
                    "status": "Success",
                    "message": "Area retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Area not found"}]
                response_data = {"records": []}
                return (
                    json.loads(
                        APIResponse(data=response_data, errors=error_response).to_json()
                    ),
                    200,
                )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
