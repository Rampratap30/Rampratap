import json
import os
import urllib.request

from dotenv import find_dotenv, load_dotenv
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import engine

from app import *
from app.lib.aws.logger import logger
from app.lib.core.database.connection_details import connectionDetails
from app.lib.exception.error_handler import errorHandler

db_engine: engine
db_tables: any
cognito_keys: list
log: logger


def initialize_app() -> (Flask, Api):
    try:
        global log
        app = Flask(__name__)
        api = Api(app)
        CORS(app)
        errorHandler(app)
        load_dotenv(find_dotenv())
        initialize_db()
        initialize_api(app)
        set_cognito_keys()
        log = logger()
        return app, api
    except Exception as err:
        err.args += tuple(["Error in Initializing app"])
        raise err


def initialize_db() -> any:
    try:
        global db_engine
        global db_tables
        db_engine, db_tables = connectionDetails.initializeDB()
    except Exception as err:
        err.args += tuple(["Error in Initializing DB"])
        raise err


def initialize_api(app: Flask) -> any:
    try:
        api_router = Blueprint("api", __name__)
        api_router.register_blueprint(home_router, url_prefix="/api/home")
        api_router.register_blueprint(changes_router, url_prefix="/api/changes")
        api_router.register_blueprint(employee_router, url_prefix="/api/employee")
        api_router.register_blueprint(view_router, url_prefix="/api/view")
        api_router.register_blueprint(report_router, url_prefix="/api/reports")
        api_router.register_blueprint(region_router, url_prefix="/api/config/region")
        api_router.register_blueprint(area_router, url_prefix="/api/config/area")
        api_router.register_blueprint(
            location_router, url_prefix="/api/config/location"
        )
        api_router.register_blueprint(
            job_code_router, url_prefix="/api/config/job-code"
        )
        api_router.register_blueprint(
            team_type_router, url_prefix="/api/config/team-type"
        )

        api_router.register_blueprint(common_router, url_prefix="/api/config/common")
        api_router.register_blueprint(
            notification_router, url_prefix="/api/config/notificaion_set_up/"
        )

        api_router.register_blueprint(log_router, url_prefix="/api/logs")

        CORS(api_router)
        app.register_blueprint(api_router)
    except Exception as err:
        err.args += tuple(["Error in Initializing DB"])
        raise err


def set_cognito_keys():
    try:
        region = os.getenv("AWS_REGION")
        userpool_id = os.getenv("AWS_USER_POOL_ID")
        keys_url = (
            "https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json".format(
                region, userpool_id
            )
        )
        with urllib.request.urlopen(keys_url) as f:
            response = f.read()
        global cognito_keys
        cognito_keys = json.loads(response.decode("utf-8"))["keys"]

    except Exception as e:
        raise e
