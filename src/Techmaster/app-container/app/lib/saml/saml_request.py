import calendar
import os
from datetime import datetime as dt, timezone
from functools import wraps
from urllib.parse import urlparse

from Cryptodome.Random import get_random_bytes
from flask import redirect, request, session
from app.lib.aws.cognito_manager import cognitoManager
from onelogin.saml2.auth import OneLogin_Saml2_Auth


class samlRequest:
    @staticmethod
    def get_auth_details(req):
        try:
            get_req = samlRequest.prepare_flask_request(req)
            auth = samlRequest.init_saml_auth(get_req)
            return auth, get_req
        except Exception as err:
            err.args += tuple(["Error in get_auth_details"])
            raise err

    @staticmethod
    def prepare_flask_request(req):
        try:
            url_data = urlparse(req.url)
            return {
                "https": "on",
                "http_host": req.host,
                "server_port": url_data.port,
                "script_name": req.path,
                "get_data": req.args.copy(),
                "post_data": req.form.copy(),
                "query_string": req.query_string,
            }
        except Exception as err:
            err.args += tuple(["Error in prepare_flask_request"])
            raise err

    @staticmethod
    def init_saml_auth(req):
        try:
            auth = OneLogin_Saml2_Auth(req, custom_base_path=os.getenv("SAML_PATH"))
            return auth
        except Exception as err:
            err.args += tuple(["Error in init_saml_auth"])
            raise err

    @staticmethod
    def set_session(auth, expiry_time_utc, token, aws_api_url):
        try:
            session["samlUserdata"] = auth.get_attributes()
            session["samlNameId"] = auth.get_nameid()
            session["samlNameIdFormat"] = auth.get_nameid_format()
            session["samlNameIdNameQualifier"] = auth.get_nameid_nq()
            session["samlNameIdSPNameQualifier"] = auth.get_nameid_spnq()
            session["samlSessionIndex"] = auth.get_session_index()
            session["employeeID"] = (auth.get_attributes())["emp_id"]
            session["NotOnOrAfter"] = auth.get_last_assertion_not_on_or_after()
            session["isAuthenticated"] = True
            session["token"] = token
            session["token_expiry_in"] = expiry_time_utc
            session["awsApiUrl"] = aws_api_url
            session["aesKey"] = get_random_bytes(16)
        except Exception as err:
            err.args += tuple(["Error in set_session"])
            raise err

    @classmethod
    def main_auth(cls, func):
        try:

            @wraps(func)
            def decorated_function(*args, **kwargs):
                try:
                    auth = cls.get_auth_details(request)[0]
                    if session.get("isAuthenticated") is not None:
                        if session["isAuthenticated"]:
                            return func(*args, **kwargs)
                        else:
                            if session:
                                session.clear()
                            return redirect(auth.login())
                    else:
                        if session:
                            session.clear()
                        return redirect(auth.login())
                except:
                    raise

            return decorated_function
        except Exception as err:
            err.args += tuple(["Error in validate_auth"])
            raise err

    @staticmethod
    def validate_auth(func):
        try:

            @wraps(func)
            def decorated_function(*args, **kwargs):
                try:
                    if session.get("isAuthenticated") is not None:
                        if session["isAuthenticated"]:
                            expiry_time_utc = session.get("token_expiry_in")
                            current_time = dt.utcnow()

                            if expiry_time_utc <= current_time:
                                (
                                    expiry_time_utc,
                                    token,
                                    aws_api_url,
                                ) = cognitoManager.getToken()
                                session["token"] = token
                                session["token_expiry_in"] = expiry_time_utc
                                session["awsApiUrl"] = aws_api_url
                            return func(*args, **kwargs)
                        else:
                            if session:
                                session.clear()
                            # return redirect(os.getenv("LOGIN_URL"))
                            return {"message": "The incoming token has expired"}, 401
                    else:
                        if session:
                            session.clear()
                        # return redirect(os.getenv("LOGIN_URL"))
                        return {"message": "The incoming token has expired"}, 401
                except:
                    raise

            return decorated_function
        except Exception as err:
            err.args += tuple(["Error in validate_auth"])
            raise err
