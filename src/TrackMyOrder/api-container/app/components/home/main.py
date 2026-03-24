import json
from flask import Blueprint, request
import initialize
import oracledb
from app.lib.request.request_validation import RequestValidation

home_router = Blueprint("home", __name__)


@home_router.route("/getdata", methods=["GET"], strict_slashes=False)
@RequestValidation.validate
def get_data():
    try:
        query_parm = request.args.get("param")
        initialize.log.write_log(query_parm)
        if query_parm == "":
            initialize.log.write_log(str(query_parm) + "Invalid Input")
            return "Invalid Input", 400
        with initialize.connection_pool.acquire() as connection:
            with connection.cursor() as cursor:
                order_details_type = connection.gettype("RAC_CI2141_ORD_DET_ARR")
                order_details = order_details_type.newobject()
                cursor.callproc(
                    "RAC_CI2141_DELIVERY_URL_LINK_PKG.order_details_out_p",
                    [query_parm, order_details],
                )
                result = get_json_fromdb(order_details)
        return result, 200
    except Exception as e:
        initialize.log.write_log("Error exists : " + str(query_parm) + str(e))
        error_response = {
            "status": "Failed",
            "message": "Error exists, Check the log message.",
        }
        return error_response, 500


def get_db_records(obj) -> dict:
    try:
        lv_column = {}
        if obj.type.iscollection:
            return is_eligible_collection_data(obj)

        else:
            for attr in obj.type.attributes:
                value = getattr(obj, attr.name)

                if isinstance(value, oracledb.Object):
                    lv_column[str(attr.name).lower()] = get_db_records(value)
                elif isinstance(value, (list, tuple)):
                    array_data = [
                        get_db_records(v) if isinstance(v, oracledb.Object) else v
                        for v in value
                    ]
                    lv_column[str(attr.name).lower()] = array_data
                else:
                    lv_column[str(attr.name).lower()] = value

        return lv_column
    except Exception as err:
        initialize.log.write_log(str(err))
        raise ValueError(f"Error while converting DB object to JSON: {err}")


def get_json_fromdb(order_details) -> json:
    try:
        lv_column = {}

        if order_details.aslist():
            lv_rows = get_db_records(order_details)
            if lv_rows:
                lv_column["data"] = lv_rows[0] if len(lv_rows) == 1 else lv_rows
            else:
                lv_column["data"] = None
        else:
            lv_column["data"] = None
        if lv_column["data"]:
            initialize.log.write_log(
                "Order Number :"
                + str(
                    lv_column["data"]["order_number"]
                    if lv_column["data"]["order_number"]
                    else "Not found"
                )
            )
        else:
            initialize.log.write_log("Error : Data not found for given param")

        return json.dumps(lv_column, indent=4)

    except Exception as err:
        initialize.log.write_log(str(err))
        raise ValueError(f"Error while converting DB object to JSON: {err}")


def is_eligible_collection_data(obj):
    collection_data = []
    for value in obj.aslist():
        if isinstance(value, oracledb.Object):
            nested_records = get_db_records(value)
            collection_data.append(nested_records)
        else:
            collection_data.append(value)
    return collection_data
