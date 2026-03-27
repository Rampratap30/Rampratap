import base64
import os
import time

import requests
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from flask import session
from flask_restful import Resource, request

from app import samlRequest


def decryptAES(data: str) -> bytes:
    key = session["aesKey"]
    content = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, key)
    q = cipher.decrypt(content).decode("utf-8")
    return unpad(q.encode(), 16, "pkcs7")


class regionalAPIGet(Resource):
    method_decorators = [samlRequest.validate_auth]

    def get(self, *args, **kwargs):
        try:
            token = session["token"]
            aws_api_url = session["awsApiUrl"]
            req_path = request.full_path.split("?")
            query_parm = ""
            if len(req_path) > 1 and req_path[1] != "":
                query_parm = str(decryptAES(req_path[1]).decode())[1:][:-1]
            headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
            api_response = requests.get(
                aws_api_url + req_path[0] + "?" + query_parm, headers=headers
            )
            if api_response.status_code == 502:
                time.sleep(2)
                api_response = requests.get(
                    aws_api_url + req_path[0] + "?" + query_parm, headers=headers
                )
            if api_response.status_code == 401:
                session.clear()
                return {"message": "The incoming token has expired"}, 401
            if str(api_response.status_code).startswith("2"):
                return api_response.json(), api_response.status_code
            else:
                try:
                    if api_response.json():
                        return api_response.json(), api_response.status_code
                except:
                    return {"message": "Error in API call"}, api_response.status_code
        except Exception as error:
            error.args += tuple(["Error in Get data from API"])
            raise error


class regionalAPIPost(Resource):
    method_decorators = [samlRequest.validate_auth]

    def post(self, *args, **kwargs):
        try:
            token = session["token"]
            aws_api_url = session["awsApiUrl"]
            logged_in_user_id = str(session["employeeID"][0])
            logged_in_email_id = session["samlNameId"]
            req_path = request.full_path.split("?")
            query_parm = ""
            if len(req_path) > 1 and req_path[1] != "":
                query_parm = str(decryptAES(req_path[1]).decode())[1:][:-1]
            headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            request.json["logged_in_user_id"] = logged_in_user_id
            request.json["logged_in_email_id"] = logged_in_email_id
            api_response = requests.post(
                aws_api_url + req_path[0] + "?" + query_parm,
                headers=headers,
                json=request.json,
            )
            if api_response.status_code == 401:
                session.clear()
                return {"message": "The incoming token has expired"}, 401
            if str(api_response.status_code).startswith("2"):
                return api_response.json(), api_response.status_code
            else:
                try:
                    if api_response.json():
                        return api_response.json(), api_response.status_code
                except:
                    return {"message": "Error in API call"}, api_response.status_code

        except Exception as error:
            error.args += tuple(["Error in POST data from API"])
            raise error


class regionalAPIPut(Resource):
    method_decorators = [samlRequest.validate_auth]

    def put(self, *args, **kwargs):
        try:
            token = session["token"]
            aws_api_url = session["awsApiUrl"]
            logged_in_user_id = str(session["employeeID"][0])
            logged_in_email_id = session["samlNameId"]
            req_path = request.full_path.split("?")
            query_parm = ""
            if len(req_path) > 1 and req_path[1] != "":
                query_parm = str(decryptAES(req_path[1]).decode())[1:][:-1]
            headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            request.json["logged_in_user_id"] = logged_in_user_id
            request.json["logged_in_email_id"] = logged_in_email_id
            api_response = requests.put(
                aws_api_url + req_path[0] + "?" + query_parm,
                headers=headers,
                json=request.json,
            )
            if api_response.status_code == 401:
                session.clear()
                return {"message": "The incoming token has expired"}, 401
            if str(api_response.status_code).startswith("2"):
                return api_response.json(), api_response.status_code
            else:
                try:
                    if api_response.json():
                        return api_response.json(), api_response.status_code
                except:
                    return {"message": "Error in API call"}, api_response.status_code
        except Exception as error:
            error.args += tuple(["Error in PUT data from API"])
            raise error
