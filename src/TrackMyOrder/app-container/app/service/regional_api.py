from datetime import datetime as dt, timezone
import time

import requests
from flask import session
from flask_restful import Resource, request
from app import CognitoManager
import initialize


class RegionalAPIGet(Resource):
    def get(self, *args, **kwargs):
        try:
            current_time = dt.now(timezone.utc)
            if not initialize.expiry_time_utc:
                initialize.expiry_time_utc, initialize.token, initialize.aws_api_url = (
                    CognitoManager.get_token()
                )
                initialize.log.write_log("Token Generated")
            elif initialize.expiry_time_utc < current_time:
                initialize.expiry_time_utc, initialize.token, initialize.aws_api_url = (
                    CognitoManager.get_token()
                )
                initialize.log.write_log("Token Generated")

            req_path = request.full_path.split("?")
            query_parm = ""
            if len(req_path) > 1 and req_path[1] != "":
                query_parm = req_path[1]
            headers = {
                "Authorization": "Bearer " + initialize.token,
                "Accept": "application/json",
            }
            initialize.log.write_log("Processing for Param : " + str(query_parm))

            api_response = requests.get(
                initialize.aws_api_url + req_path[0] + "?" + query_parm, headers=headers
            )

            initialize.log.write_log(
                "api_response.status_code : " + str(api_response.status_code)
            )

            if api_response.status_code == 502:
                time.sleep(2)
                api_response = requests.get(
                    initialize.aws_api_url + req_path[0] + "?" + query_parm,
                    headers=headers,
                )
                initialize.log.write_log(
                    "Retry api_response.status_code : " + str(api_response.status_code)
                )
            if api_response.status_code == 401:
                initialize.log.write_log("The incoming token has expired")
                return {"message": "The incoming token has expired"}, 401
            if str(api_response.status_code).startswith("2"):
                return api_response.json(), api_response.status_code
            else:
                try:
                    if api_response.json():
                        return api_response.json(), api_response.status_code
                except Exception as error:
                    initialize.log.write_log("Error in API call.")
                    return {"message": "Error in API call"}, api_response.status_code
        except Exception as error:
            initialize.log.write_log("Error in API call." + str(error))
            error.args += tuple(["Error in Get data from API"])
            raise error
