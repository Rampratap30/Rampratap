import json
from datetime import date as dates
from datetime import datetime as dt

from flask import Blueprint, request
from sqlalchemy import desc, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

location_router = Blueprint("location", __name__)


# Get location count
@location_router.route("/get_count", methods=["GET"])
@requestValidation.validate
def get_count():
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_LOC, session)
            location_count = service.get_count()
            return (
                json.loads(
                    APIResponse(
                        data={
                            "count": location_count,
                            "status": "Success",
                            "message": "location Count retrieved successfully",
                        }
                    ).to_json()
                ),
                200,
            )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get location details based on location, status and pagination
@location_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_location_pagination():
    try:
        location_name = request.args.get("location_name")
        status = request.args.get("status")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "last_update_date")
        order = request.args.get("order", "desc").lower()
        is_export_all = request.args.get("is_export_all", "N")

        with dbSession() as session:
            tab_location = aliased(initialize.db_tables.RAC_FS_TM_LOC)
            query = session.query(
                tab_location.LOC_ID,
                tab_location.LOCATION_CODE,
                tab_location.DESCRIPTION,
                tab_location.ZIP_CODE,
                tab_location.INACTIVE_DATE,
                tab_location.LAST_UPDATE_DATE.label("LAST_UPDATE_DATE"),
            )
            total_items = 0
            if is_export_all != "Y":
                if location_name:
                    query = query.filter(
                        tab_location.LOCATION_CODE.ilike(f"%{location_name}%")
                    )
                if status:
                    if status == "Y":
                        query = query.filter(tab_location.INACTIVE_DATE != None)
                    else:
                        query = query.filter(tab_location.INACTIVE_DATE == None)
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
                    if status == "Y":
                        query = query.filter(tab_location.INACTIVE_DATE != None)
                    else:
                        query = query.filter(tab_location.INACTIVE_DATE == None)
                total_items = query.count()
                results = query.all()

            if results:
                response_data = {
                    "records": [
                        {
                            "location_id": result.LOC_ID,
                            "location_code": result.LOCATION_CODE,
                            "description": result.DESCRIPTION,
                            "zip_code": result.ZIP_CODE,
                            "inactive_date": dates.strftime(
                                result.INACTIVE_DATE, "%m-%d-%Y"
                            )
                            if result.INACTIVE_DATE is not None
                            else result.INACTIVE_DATE,
                        }
                        for result in results
                    ],
                    "total_items": total_items,
                    "page": page,
                    "per_page": per_page,
                    "order_by": order_by,
                    "order": order,
                    "status": "Success",
                    "message": "location retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Location not found"}]
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


# Get location details based on location id
@location_router.route("/get/<int:location_id>", methods=["GET"])
@requestValidation.validate
def get_location_by_id(location_id: int):
    try:
        with dbSession() as session:
            tab_location = aliased(initialize.db_tables.RAC_FS_TM_LOC)
            results = (
                session.query(
                    tab_location.LOC_ID,
                    tab_location.LOCATION_CODE,
                    tab_location.DESCRIPTION,
                    tab_location.ZIP_CODE,
                    tab_location.INACTIVE_DATE,
                )
                .filter(tab_location.LOC_ID == location_id)
                .all()
            )

            if results:
                response_data = {
                    "records": [
                        {
                            "location_id": result.LOC_ID,
                            "location_code": result.LOCATION_CODE,
                            "description": result.DESCRIPTION,
                            "zip_code": result.ZIP_CODE,
                            "inactive_date": dates.strftime(
                                result.INACTIVE_DATE, "%m-%d-%Y"
                            )
                            if result.INACTIVE_DATE is not None
                            else result.INACTIVE_DATE,
                        }
                        for result in results
                    ],
                    "status": "Success",
                    "message": "location retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Location not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
