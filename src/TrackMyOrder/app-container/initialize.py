from datetime import datetime as dt

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from app import ErrorHandler, logger, GenerateAPIUrl, RegionalAPIGet

log: logger
expiry_time_utc: dt = None
token: str = None
aws_api_url: str = None


def initialize_app() -> Flask:
    try:
        global log
        log = logger()
        app = Flask(__name__)
        api = Api(app)
        CORS(app, resources={r"*": {"origins": "*"}})
        load_dotenv(find_dotenv())
        ErrorHandler(app, log)
        api_url = GenerateAPIUrl()
        log.write_log("generateAPIUrl completed sucessfully.")
        api.add_resource(RegionalAPIGet, *api_url.get_url)
        log.write_log("Initialize_app completed sucessfully.")
        log.write_log("Starting Application Log")
        return app
    except Exception as err:
        err.args += tuple(["Error in Initializing app"])
        raise err
