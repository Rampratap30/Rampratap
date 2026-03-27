import json
import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.automap import automap_base

from app.lib.aws.secret_manager import secretManager


class connectionDetails:
    @staticmethod
    def initializeDB():
        try:
            secretDit = secretManager.get_value(os.getenv("AWS_SECRETS_MYSQL"))
            dbUrl = URL.create(
                "mysql+mysqlconnector",
                username=secretDit["username"],
                password=secretDit["password"],
                host=secretDit["host"],
                port=secretDit["port"],
                database=secretDit["dbname"],
            )
            engine = create_engine(
                dbUrl,
                pool_pre_ping=True,
                echo=bool(os.getenv("SQL_LOG")),
                logging_name=os.getenv("SQL_LOG_NAME"),
            )
            metadata = MetaData()
            mainDir = "app/lib/core/database/"
            f = open(mainDir + "tables.json")
            tm_tables = json.load(f)
            metadata.reflect(engine, only=tm_tables["tables"])
            base = automap_base(metadata=metadata)
            base.prepare()
            tables = base.classes
            return engine, tables
        except Exception as e:
            raise e
