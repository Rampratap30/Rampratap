import json
from datetime import date as dates
from datetime import datetime
from datetime import datetime as dt

from flask import Blueprint, request
from sqlalchemy import desc, or_, text
from sqlalchemy.orm import aliased

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_notif import (
    racFsTmNotificationCreate,
    racFsTmNotificationUpdate,
)
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse

notification_router = Blueprint("notification", __name__)


# Get Notification count
@notification_router.route("/get_count", methods=["GET"])
@requestValidation.validate
def get_count():
    try:
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_NOTIF, session)
            notification_count = service.get_count()
            return (
                json.loads(
                    APIResponse(
                        data={
                            "count": notification_count,
                            "status": "Success",
                            "message": "Notification Count retrieved successfully",
                        }
                    ).to_json()
                ),
                200,
            )
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Get Notification details based on notification, status and pagination
@notification_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_notification_pagination():
    try:
        notification_name = request.args.get("notification_name")
        status = request.args.get("status")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "last_update_date")
        order = request.args.get("order", "desc").lower()
        is_export_all = request.args.get("is_export_all", "N")
        with dbSession() as session:
            tab_notification = aliased(initialize.db_tables.RAC_FS_TM_NOTIF)
            query = session.query(
                tab_notification.NOTIFICATION_ID,
                tab_notification.NOTIFICATION_NAME,
                tab_notification.EMAIL_ID,
                tab_notification.NOTIFICATION_SUBJECT,
                tab_notification.EFFECTIVE_START_DATE,
                tab_notification.EFFECTIVE_END_DATE,
                tab_notification.STATUS,
                tab_notification.LAST_UPDATE_DATE.label("LAST_UPDATE_DATE"),
            )
            total_items = 0
            if is_export_all != "Y":
                if notification_name:
                    query = query.filter(
                        tab_notification.NOTIFICATION_NAME.like(
                            f"%{notification_name}%"
                        )
                    )
                if status:
                    query = query.filter(tab_notification.STATUS == status)
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
                    query = query.filter(tab_notification.STATUS == status)
                total_items = query.count()
                results = query.all()
            if results:
                response_data = {
                    "records": [
                        {
                            "notification_id": result.NOTIFICATION_ID,
                            "notification_name": result.NOTIFICATION_NAME,
                            "notification_email_id": result.EMAIL_ID,
                            "notification_subject": result.NOTIFICATION_SUBJECT,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_START_DATE
                            else None,
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE
                            else None,
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
                    "message": "Notification retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [
                    {"status": "Failed", "message": "Notification not found"}
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


# Get Notification details based on notification id
@notification_router.route("/get/<int:notification_id>", methods=["GET"])
@requestValidation.validate
def get_notification_by_id(notification_id: int):
    try:
        with dbSession() as session:
            tab_notification = aliased(initialize.db_tables.RAC_FS_TM_NOTIF)
            results = (
                session.query(
                    tab_notification.NOTIFICATION_ID,
                    tab_notification.NOTIFICATION_NAME,
                    tab_notification.EMAIL_ID,
                    tab_notification.NOTIFICATION_SUBJECT,
                    tab_notification.EFFECTIVE_START_DATE,
                    tab_notification.EFFECTIVE_END_DATE,
                    tab_notification.STATUS,
                )
                .filter(tab_notification.NOTIFICATION_ID == notification_id)
                .all()
            )
            if results:
                response_data = {
                    "records": [
                        {
                            "notification_id": result.NOTIFICATION_ID,
                            "notification_name": result.NOTIFICATION_NAME,
                            "notification_email_id": result.EMAIL_ID,
                            "notification_subject": result.NOTIFICATION_SUBJECT,
                            "effective_start_date": dates.strftime(
                                result.EFFECTIVE_START_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_START_DATE
                            else None,
                            "effective_end_date": dates.strftime(
                                result.EFFECTIVE_END_DATE, "%m-%d-%Y"
                            )
                            if result.EFFECTIVE_END_DATE
                            else None,
                            "status": result.STATUS,
                        }
                        for result in results
                    ],
                    "status": "Success",
                    "message": "Notification retrieved successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [{"status": "Failed", "message": "Region not found"}]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Create new notification
@notification_router.route("/add", methods=["POST"])
@requestValidation.validate
def add_notification():
    try:
        data = request.json
        with dbSession() as session:
            if "effective_start_date" in data:
                current_time = dt.now().strftime("%H:%M:%S")
                data["effective_start_date"] += f"T{current_time}"
                service = baseService(initialize.db_tables.RAC_FS_TM_NOTIF, session)
                row = service.create(racFsTmNotificationCreate(**data))
                response_data = {
                    "records": [{"notification_id": row.NOTIFICATION_ID}],
                    "status": "Success",
                    "message": "Notification created successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 201
            else:
                response_data = {
                    "status": "Failed",
                    "message": "effective_start_date is mandatory",
                }
                return json.loads(APIResponse(errors=response_data).to_json()), 400

    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Update existing Notification
@notification_router.route("/update/<int:notification_id>", methods=["PUT"])
@requestValidation.validate
def update_notification(notification_id: int):
    try:
        data = request.json
        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_NOTIF, session)
            notification = service.get_pk_id(notification_id)
            if notification:
                if "effective_start_date" in data:
                    current_time = dt.utcnow().strftime("%H:%M:%S")
                    data["effective_start_date"] += f"T{current_time}"
                else:
                    data["effective_start_date"] = notification.EFFECTIVE_START_DATE

                if data["status"] == "INACTIVE":
                    current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    data["effective_end_date"] = current_datetime_utc
                else:
                    data["effective_end_date"] = None
                notification_update = service.update(
                    notification, racFsTmNotificationUpdate(**data)
                )
                response_data = {
                    "records": [
                        {"notification_id": notification_update.NOTIFICATION_ID}
                    ],
                    "status": "Success",
                    "message": "Notification updated successfully",
                }
                return json.loads(APIResponse(data=response_data).to_json()), 200
            else:
                error_response = [
                    {"status": "Failed", "message": "Notification not found"}
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 404
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500


# Bulk Delete
@notification_router.route("/update/bulk-delete", methods=["PUT"])
@requestValidation.validate
def bulk_delete():
    try:
        data = request.json
        if "notification_id" not in data or "logged_in_user_id" not in data:
            error_response = [
                {
                    "status": "Failed",
                    "message": "Missing required fields 'notification_id' or 'logged_in_user_id'.",
                }
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        notification_ids = data["notification_id"]
        logged_in_user_id = data["logged_in_user_id"]

        if not notification_ids:
            error_response = [
                {"status": "Failed", "message": "notification_id list cannot be empty."}
            ]
            return json.loads(APIResponse(errors=error_response).to_json()), 400

        with dbSession() as session:
            service = baseService(initialize.db_tables.RAC_FS_TM_NOTIF, session)
            current_datetime_utc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            for notification_id in notification_ids:
                session.query(service.model).filter(
                    service.model.NOTIFICATION_ID == notification_id
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
                "records": [{"notification_id": notification_ids}],
                "status": "Success",
                "message": "Notification(s) deactivated successfully",
            }
            return json.loads(APIResponse(data=response_data).to_json()), 200
    except Exception as e:
        error_response = [{"status": "Failed", "message": str(e)}]
        return json.loads(APIResponse(errors=error_response).to_json()), 500
