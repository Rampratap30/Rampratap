import json
import os
from datetime import date as dates
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy import desc, func, or_, text
from sqlalchemy.orm import aliased
from sqlalchemy.sql import null
from sqlalchemy.sql.expression import literal

import initialize
from app.lib.core.database.db_session import dbSession
from app.lib.core.schemas.rac_fs_tm_logs import racFsTmLogsCreate, racFsTmLogsUpdate
from app.lib.core.services.base_service import baseService
from app.lib.request.request_validation import requestValidation
from app.lib.response.api_response import APIResponse
from app.lib.aws.aws_lambda import awsLambda

log_router = Blueprint("log", __name__)


# This endpoint will be used for the changes page filter section.
@log_router.route("/get", methods=["GET"])
@requestValidation.validate
def get_log():
    try:
        # Extract query parameters from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        order_by = request.args.get("order_by", "CREATION_DATE")
        order = request.args.get("order", "desc").lower()
        from_date = request.args.get("from_date")
        to_date = request.args.get("to_date")
        types = request.args.get("type")
        search_emp_id = request.args.get("search_emp_id")
        is_export_all = request.args.get("is_export_all", "N")

        # Start a database session
        with dbSession() as session:
            # Create aliases for database tables
            tab_log = aliased(initialize.db_tables.RAC_FS_TM_LOGS, name="log")
            tab_sync_log = aliased(
                initialize.db_tables.RAC_FS_TM_SYNC_LOGS, name="syncLog"
            )

            # Build the query to fetch data
            query1 = session.query(
                null().label("EMPLOYEE_ID"),
                null().label("RESOURCE_NUMBER"),
                tab_log.EMAIL_ID,
                tab_log.FILE_NAME,
                tab_log.LAMBDA_STATUS,
                tab_log.MSG,
                tab_log.TYPE,
                func.RAC_FS_TM_GET_USER_NAME(tab_log.CREATED_BY).label("CREATED_BY"),
                tab_log.CREATION_DATE.label("CREATION_DATE"),
            ).filter(tab_log.TYPE.in_(("Bulk Import", "home", "LOG")))
            if types:
                query1 = query1.filter(tab_log.TYPE == types)
            if from_date and to_date:
                date = datetime.strptime(to_date, "%Y-%m-%d")
                # endDate = date + timedelta(days=1)
                query1 = query1.filter(
                    tab_log.CREATION_DATE.between(
                        from_date + " 00:00:00", to_date + " 23:59:59"
                    )
                )
            query2 = session.query(
                tab_sync_log.EMPLOYEE_ID,
                tab_sync_log.RESOURCE_NUMBER,
                tab_sync_log.LOGIN,
                null().label("FILE_NAME"),
                null().label("LAMBDA_STATUS"),
                tab_sync_log.ERR_MSG,
                tab_sync_log.SYNC_PROCESS,
                func.RAC_FS_TM_GET_USER_NAME(tab_sync_log.CREATED_BY).label(
                    "CREATED_BY"
                ),
                tab_sync_log.CREATION_DATE.label("CREATION_DATE"),
            ).filter(tab_sync_log.SYNC_PROCESS.in_(("HRMS", "OFSC")))
            if types:
                query2 = query2.filter(tab_sync_log.SYNC_PROCESS == types)
            if search_emp_id:
                query2 = query2.filter(tab_sync_log.EMPLOYEE_ID == search_emp_id)
            if from_date and to_date:
                date = datetime.strptime(to_date, "%Y-%m-%d")
                # endDate = date + timedelta(days=1)
                query2 = query2.filter(
                    tab_sync_log.CREATION_DATE.between(
                        from_date + " 00:00:00", to_date + " 23:59:59"
                    )
                )

            query = query1.union(query2)

            if is_export_all != "Y":
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
                        "email_id": result.EMAIL_ID,
                        "file_name": result.FILE_NAME,
                        "lambda_status": result.LAMBDA_STATUS,
                        "message": result.MSG,
                        "type": result.TYPE,
                        "created_by": result.CREATED_BY,
                        "created_date": dates.strftime(result.CREATION_DATE, "%m-%d-%Y")
                        if result.CREATION_DATE
                        else None,
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


@log_router.route("/bulk_export", methods=["POST"])
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
