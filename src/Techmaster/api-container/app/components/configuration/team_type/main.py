import json
from datetime import date as dates
from datetime import datetime as dt

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_team_type import (
    racFsTmTeamTypeCreate,
    racFsTmTeamTypeUpdate,
)
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

team_type_router = Blueprint("team_type", __name__)


# Get team_type count
@team_type_router.route("/get_count", methods=["GET"])
@requestValidation.validate
def get_count():
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, session)
            team_type_count = service.get_count()
            return (
                json.loads(
                    APIResponse(
                        data={
                            "count": team_type_count,
                            "status": "Success",
                            "message": "team_type Count retrieved successfully",
                        }
                    ).to_json()
                ),
                200,
            )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get team_type details based on team_type, status and pagination
@team_type_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_team_type_pagination():
    try:
        team_type_name = request.args.get("team_type_name")
        status = request.args.get("status")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "last_update_date")
        order = request.args.get("order", "desc").lower()
        is_export_all = request.args.get("is_export_all", "N")

        with dbSession() as session:
            tab_team_type = aliased(initialize.db_tables.RAC_FS_TM_TEAM_TYPE)
            query = session.query(
                tab_team_type.TEAM_TYPE_ID,
                tab_team_type.TEAM_TYPE_NAME,
                tab_team_type.EFFECTIVE_START_DATE,
                tab_team_type.EFFECTIVE_END_DATE,
                tab_team_type.STATUS,
                tab_team_type.LAST_UPDATE_DATE.label("LAST_UPDATE_DATE"),
            )
            total_items = 0
            if is_export_all != "Y":
                if team_type_name:
                    query = query.filter(
                        tab_team_type.TEAM_TYPE_NAME.ilike(f"%{team_type_name}%")
                    )
                if status:
                    query = query.filter(tab_team_type.STATUS == status)
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
                    query = query.filter(tab_team_type.STATUS == status)
                total_items = query.count()
                results = query.all()

            if results:
                response_data = {
                    "records": [
                        {
                            "team_type_id": result.TEAM_TYPE_ID,
                            "team_type_name": result.TEAM_TYPE_NAME,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
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
                    "message": "Team Type retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [
                    {"status": "Failed", "message": "Team Type not found"}
                ]
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


# Get team_type details based on team_type id
@team_type_router.route("/get/<int:team_type_id>", methods=["GET"])
@requestValidation.validate
def get_team_type_by_id(team_type_id: int):
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, session)
            result = service.get_pk_id(team_type_id)
            if result:
                response_data = {
                    "records": [
                        {
                            "team_type_id": result.TEAM_TYPE_ID,
                            "team_type_name": result.TEAM_TYPE_NAME,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            ),
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE is not None
                            else result.EFFECTIVE_END_DATE,
                            "status": result.STATUS,
                        }
                    ],
                    "status": "Success",
                    "message": "Team Type retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [
                    {"status": "Failed", "message": "Team Type not found"}
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Create new team_type
@team_type_router.route("/add", methods=["POST"])
@requestValidation.validate
def add_team_type():
    try:
        data = request.json

        with dbSession() as session:
            if "effective_start_date" in data:
                current_time = dt.utcnow().strftime("%H:%M:%S")
                data["effective_start_date"] += f"T{current_time}"
                service = baseService(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, session)
                row = service.create(racFsTmTeamTypeCreate(**data))
                response_data = {
                    "records": [{"team_type_id": row.TEAM_TYPE_ID}],
                    "status": "Success",
                    "message": "team_type created successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 201
            else:
                response_data = {
                    "status": "Failed",
                    "message": "EFFECTIVE_START_DATE is mandatory",
                }
                return json.loads(APIResponse(errors=response_data).to_json()), 400

    except IntegrityError as e:
        error_response = [
            {"status": "Failed", "message": "Team Type already exists in our record."}
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Update existing team_type
@team_type_router.route("/update/<int:team_type_id>", methods=["PUT"])
@requestValidation.validate
def update_team_type(team_type_id: int):
    try:
        data = request.json
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, session)
            team_type_row = service.get_pk_id(team_type_id)
            if team_type_row:
                if "effective_start_date" in data:
                    current_time = dt.utcnow().strftime("%H:%M:%S")
                    data["effective_start_date"] += f"T{current_time}"
                else:
                    data["effective_start_date"] = team_type_row.EFFECTIVE_START_DATE

                if data["status"] == "INACTIVE":
                    current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    data["effective_end_date"] = current_datetime_utc
                else:
                    data["effective_end_date"] = None

                row = service.update(team_type_row, racFsTmTeamTypeUpdate(**data))
                response_data = {
                    "records": [{"team_type_id": row.TEAM_TYPE_ID}],
                    "status": "Success",
                    "message": "team_type updated successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [
                    {"status": "Failed", "message": "team_type not found"}
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except IntegrityError as e:
        error_response = [
            {"status": "Failed", "message": "Team Type already exists in our record."}
        ]
        return json.loads(APIResponse(errors=error_response).to_json()), 400
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Bulk Delete
@team_type_router.route("/update/bulk-delete", methods=["PUT"])
@requestValidation.validate
def bulk_delete():
    try:
        data = request.json
        print(data)
        if "team_type_id" not in data or "logged_in_user_id" not in data:
            error_response = [
                {
                    "status": "Failed",
                    "message": "Missing required fields 'team_type_id' or 'logged_in_user_id'.",
                }
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        team_type_ids = data["team_type_id"]
        logged_in_user_id = data["logged_in_user_id"]

        if not team_type_ids:
            error_response = [
                {"status": "Failed", "message": "team_type_id list cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_TEAM_TYPE, session)
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            for team_type_id in team_type_ids:
                session.query(service.model).filter(
                    service.model.TEAM_TYPE_ID == team_type_id
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
                "records": [{"team_type_id": team_type_ids}],
                "status": "Success",
                "message": "Team Type(s) deactivated successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
