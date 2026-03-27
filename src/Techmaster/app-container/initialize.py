import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_session import Session

from app import errorHandler, logger, techMasterAPIUrl


def initialize_app() -> (Flask, Api, logger, techMasterAPIUrl):
    try:
        flask_app = Flask(__name__)
        api = Api(flask_app)
        CORS(flask_app, resources={r"*": {"origins": "*"}})
        log = logger()
        log.write_log("Log Initialied...")
        errorHandler(flask_app, log)
        load_dotenv(find_dotenv())
        flask_app.secret_key = "TM_SSO_XDRTFC1CV"
        flask_app.config["SESSION_TYPE"] = "filesystem"
        flask_app.config["SESSION_FILE_DIR"] = "/tech-master/flask-session"
        flask_app.config["SESSION_PERMANENT"] = True
        flask_app.config["PERMANENT_SESSION_LIFETIME"] = 28800
        os.environ["SAML_PATH"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "app/lib/saml"
        )
        Session(flask_app)
        tm_api_url = techMasterAPIUrl()
        return flask_app, api, log, tm_api_url
    except Exception as err:
        err.args += tuple(["Error in Initializing app"])
        raise err
