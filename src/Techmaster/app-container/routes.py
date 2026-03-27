# ------------------------------------------------------------------------------#
# Type                  : Python												#
# File Name             : routes.py                                             #
# Purpose               : APP layer entry point                                 #
# Created By			: Hexaware                                              #
# Last Updated By       :                                                       #
#                                                                               #
# Author   	   Date       	 Ver   		Description                             #
# ---------    -----------   ------   	----------------------------------------#
# Hexaware	   26-Jun-2023   210.00		CHG0082320 - Created                    #
# ------------------------------------------------------------------------------#
import os
from datetime import datetime

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
)
from flask_restful import Api, HTTPException
from app.service.user_info import putUserInfo
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

import initialize
from app import (
    cognitoManager,
    regionalAPIGet,
    regionalAPIPost,
    regionalAPIPut,
    samlRequest,
    userInfo,
    validateUserInfo,
)
from app.service.file_import import fileUpload

flask_app, api, log, tm_api_url = initialize.initialize_app()


@flask_app.route("/status")
def server_up():
    return "Server is running! Current Server Time : {}".format(datetime.now())


@flask_app.route("/", methods=["GET"])
@samlRequest.main_auth
def index():
    return render_template("index.html")


@flask_app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(flask_app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@flask_app.route("/sso", methods=["POST", "GET"])
def sso_check():
    try:
        not_auth_warn = False
        not_in_TM_group = False
        error_reason = ""
        auth, saml_req = samlRequest.get_auth_details(request)
        if "acs" in request.args:
            auth.process_response()
            if auth.is_authenticated():
                errors = auth.get_errors()
                if len(errors) == 0:
                    expiry_time_utc, token, aws_api_url = cognitoManager.getToken()
                    samlRequest.set_session(auth, expiry_time_utc, token, aws_api_url)
                    self_url = OneLogin_Saml2_Utils.get_self_url(saml_req)
                    # Redirect to Home Page
                    user_info = validateUserInfo.validate()
                    if user_info["userRole"] != "":
                        log.write_log("Logged In User : " + user_info["userName"])
                        if (
                            "RelayState" in request.form
                            and self_url != request.form["RelayState"]
                        ):
                            return redirect(
                                auth.redirect_to(request.form["RelayState"])
                            )
                        else:
                            return render_template("index.html")
                    else:
                        error_reason = "Invalid user for Techmaster application."
                        log.write_log(error_reason)
                        not_in_TM_group = True
                        raise PermissionError
                else:
                    log.write_log(errors)
                    error_reason = auth.get_last_error_reason()
                    not_auth_warn = True
                    raise RuntimeError
            else:
                not_auth_warn = True
                log.write_log("Raise not login error")
                raise
        elif "sls" in request.args:
            request_id = None
            if "LogoutRequestID" in session:
                request_id = session["LogoutRequestID"]

            def dscb():
                return session.clear()

            url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
            errors = auth.get_errors()
            if len(errors) == 0:
                if url is not None:
                    return redirect(url)
                else:
                    success_slo = True
            elif auth.get_settings().is_debug_active():
                error_reason = auth.get_last_error_reason()
        elif "slo" in request.args:
            name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
            if "samlNameId" in session:
                name_id = session["samlNameId"]
            if "samlSessionIndex" in session:
                session_index = session["samlSessionIndex"]
            if "samlNameIdFormat" in session:
                name_id_format = session["samlNameIdFormat"]
            if "samlNameIdNameQualifier" in session:
                name_id_nq = session["samlNameIdNameQualifier"]
            if "samlNameIdSPNameQualifier" in session:
                name_id_spnq = session["samlNameIdSPNameQualifier"]
            session.clear()
            return redirect(
                auth.logout(
                    name_id=name_id,
                    session_index=session_index,
                    nq=name_id_nq,
                    name_id_format=name_id_format,
                    spnq=name_id_spnq,
                )
            )
        else:
            not_auth_warn = True
            raise
    except Exception as err:
        if not_auth_warn:
            if session:
                session.clear()
            log.write_log("not_auth_warn")
            HTTPException.code = 401
            HTTPException.description = "Kindly login."
            raise HTTPException
        elif not_in_TM_group:
            if session:
                session.clear()
            log.write_log("not_in_TM_group")
            session.clear()
            err.args += tuple([error_reason])
            raise err
        else:
            if session:
                session.clear()
            log.write_log("Error in SSO login")
            err.args += tuple(["Error in SSO login"])
            raise err


api.add_resource(userInfo, "/user-info")
api.add_resource(fileUpload, "/bulk-upload")
api.add_resource(regionalAPIGet, *tm_api_url.get_url)
api.add_resource(regionalAPIPost, *tm_api_url.post_url)
api.add_resource(regionalAPIPut, *tm_api_url.put_url)
