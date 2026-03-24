import json
import os
import urllib
import oracledb
from dotenv import find_dotenv, load_dotenv
from flask import Blueprint, Flask
from flask_cors import CORS
from app.components import home_router
from app.lib.aws.logger import logger
from app.lib.core.database.connection import ConnectionDetails

cognito_keys: list
log: logger
connection_pool: oracledb.ConnectionPool


def initialize_app() -> Flask:
    try:
        global log
        global connection_pool
        log = logger()
        # app = Flask(__name__)
        # CORS(app)
        app = Flask(__name__)
        app.config['WTF_CSRF_ENABLED'] = False # Sensitive
        CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}}) # Sensitive     
        load_dotenv(find_dotenv())
        initialize_api(app, log)
        set_cognito_keys(log)
        connection_pool = ConnectionDetails.initialize_db()
        log.write_log("Initialize_app completed sucessfully.")
        log.write_log("Starting Application Log")
        return app
    except Exception as err:
        err.args += tuple(["Error in Initializing app"])
        raise err


def initialize_api(app: Flask, log: logger) -> any:
    try:
        api_router = Blueprint("api", __name__)
        api_router.register_blueprint(home_router, url_prefix="/api/home")
        #CORS(api_router)
        app.register_blueprint(api_router)
    except Exception as err:
        log.write_log(err)
        err.args += tuple(["Error in Initializing router"])
        raise err


def set_cognito_keys(log: logger):
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

    except Exception as err:
        log.write_log(err)
        raise err
