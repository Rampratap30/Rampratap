import json
import os
import base64

import requests
from flask import Flask, make_response, redirect, render_template, request, session
from flask_restful import Resource, request

from app.lib.aws.logger import logger
from app.lib.response.api_response import APIResponse
from app.lib.saml.saml_request import samlRequest


class userInfo(Resource):
    method_decorators = [samlRequest.validate_auth]

    def get(self, *args, **kwargs):
        errorMessage = ""
        result = {}
        try:
            result = validateUserInfo.validate()
            if result["userRole"] != "":
                return json.loads(APIResponse(data=result).to_json()), 200
            else:
                return (
                    json.loads(
                        APIResponse(
                            error="User not assinged to any of the Tech Master groups."
                        ).to_json()
                    ),
                    400,
                )

        except Exception as error:
            return (
                json.loads(
                    APIResponse(
                        error="User not assinged to any of the Tech Master groups."
                    ).to_json()
                ),
                400,
            )


class validateUserInfo:
    @staticmethod
    def validate():
        result = {"userName": "", "userRole": "", "aesKey": ""}
        try:
            userRole = ""
            errorMessage = ""
            aesKey = ""
            getAttributes = session["samlUserdata"]
            userName = getAttributes[
                "http://schemas.microsoft.com/identity/claims/displayname"
            ][0]
            role = getAttributes[
                "http://schemas.microsoft.com/ws/2008/06/identity/claims/groups"
            ]
            user_id = str(session["employeeID"][0])
            if os.getenv("ADMIN_GROUP") in role:
                userRole = "ADMIN"
                aesKey = base64.b64encode(session["aesKey"]).decode()
            elif os.getenv("MANAGER_GROUP") in role:
                userRole = "MANAGER"
                aesKey = base64.b64encode(session["aesKey"]).decode()
            else:
                userRole = ""
                aesKey = ""
                session.clear()
            result["userName"] = userName
            result["userRole"] = userRole
            result["aesKey"] = aesKey
            result["user_id"] = user_id
            putUserInfo.update_user_login(result)

        except Exception as error:
            result["userName"] = ""
            result["userRole"] = ""
            result["aesKey"] = ""
            result["user_id"] = ""
            session.clear()
        finally:
            return result


class putUserInfo:
    @staticmethod
    def update_user_login(result: any):
        try:
            token = session["token"]
            aws_api_url = session["awsApiUrl"]
            data = {}
            if result["userName"]:
                data["logged_in_user_id"] = result["user_id"]
                data["logged_in_email_id"] = session["samlNameId"]
                data["logged_in_userName"] = result["userName"]
                data["logged_in_userRole"] = result["userRole"]

                req_path = "/api/home/update_user_login"
                headers = {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }

                api_response = requests.post(
                    aws_api_url + req_path,
                    headers=headers,
                    json=data,
                )
                if str(api_response.status_code).startswith("2"):
                    return api_response.json(), api_response.status_code
                else:
                    try:
                        if api_response.json():
                            return api_response.json(), api_response.status_code
                    except:
                        return {
                            "message": "Error in API call"
                        }, api_response.status_code

        except Exception as error:
            error.args += tuple(["Error in POST data from API"])
