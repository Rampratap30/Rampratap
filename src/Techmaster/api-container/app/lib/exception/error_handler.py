from flask import render_template, request

import initialize
from app.lib.response.api_response import APIResponse


class errorHandler:
    def __init__(self, app) -> None:
        @app.errorhandler(Exception)
        def app_exception_handling(err):
            # if str(err):
            #   log.write_log(str(err))
            initialize.log.write_log("API Error URL : " + request.full_path)
            initialize.log.write_log("Error :" + str(err))
            return APIResponse(
                errors=[type(err).__name__, str(err)],
            ).to_json()
