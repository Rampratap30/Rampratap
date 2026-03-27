# -------------------------------------------------------------------------------#
# Type                  : Python												#
# File Name             : request_validation.py                                 #
# Purpose               : Declare all the API details                           #
# Created By			: Sathish.Shanmugam@ricoh-usa.com                       #
# Last Updated By       :                                                       #
# #
# Author   	   Date       	 Ver   		Description                             #
# ---------    -----------   ------   	----------------------------------------#
# Hexaware	   26-Jun-2023   210.00		CHG0082320 - Created                    #
# -------------------------------------------------------------------------------#

from functools import wraps

from flask_restful import Resource, request
from jose import jwk, jwt
from jose.utils import base64url_decode

import initialize


class requestValidation:
    @staticmethod
    def validate(func):
        try:

            @wraps(func)
            def decorated_function(*args, **kwargs):
                try:
                    error_list = []
                    if "Authorization" not in request.headers:
                        error_list.append("Missing Authorization")
                        raise
                    else:
                        token = request.headers["Authorization"]
                        if token is None or token == "":
                            error_list.append("Empty Token")
                            raise
                        else:
                            if not token.startswith("Bearer"):
                                error_list.append("Missing Bearer in Authorization")
                                raise

                            else:
                                token = request.headers["Authorization"][7:]
                                if __class__.jwt_validation(token):
                                    error_list += __class__.validate_header(request)
                                    if not error_list:
                                        return func(*args, **kwargs)
                                    else:
                                        raise
                                else:
                                    error_list.append("Invalid Token")
                                    raise
                except Exception as e:
                    e.args += tuple(error_list)
                    raise e

            return decorated_function
        except Exception as e:
            raise e

    @staticmethod
    def jwt_validation(token) -> bool:
        try:
            jwt_headers = jwt.get_unverified_headers(token)
            kid = jwt_headers["kid"]
            key_index = -1
            for i in range(len(initialize.cognito_keys)):
                if kid == initialize.cognito_keys[i]["kid"]:
                    key_index = i
                    break
            if key_index == -1:
                return False

            public_key = jwk.construct(initialize.cognito_keys[key_index])
            message, encoded_signature = str(token).rsplit(".", 1)
            decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
            if not public_key.verify(message.encode("utf8"), decoded_signature):
                return False
            return True
        except Exception as e:
            raise e

    @staticmethod
    def validate_header(request) -> list:
        try:
            header_error_list = []
            headers = request.headers
            http_method = request.method
            # checking Accept
            has_accept = "Accept" in headers
            if has_accept == False:
                header_error_list.append("Expected Accept in headers")
            elif headers["Accept"] != "application/json":
                header_error_list.append(
                    ("Invalid Accept header. Expected application/json")
                )

            if http_method.upper() == "POST":
                # Checking content type
                has_content_type = "Content-Type" in headers
                if has_content_type == False:
                    header_error_list.append("Expected Content-Type in headers")

                elif headers["Content-Type"] not in (
                    "application/json",
                    "application/octet-stream",
                    "multipart/form-data",
                ):
                    header_error_list.append(
                        "Invalid Content-Type. Expected application/json"
                    )
                # Validate request body
                elif not request.data:
                    header_error_list.append(
                        "Invalid Request Body. Expected json value"
                    )
            return header_error_list
        except Exception as e:
            raise e
