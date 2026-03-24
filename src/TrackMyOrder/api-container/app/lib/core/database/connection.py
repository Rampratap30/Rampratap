import os
import oracledb
import initialize
from app.lib.aws.secret_manager import SecretManager


class ConnectionDetails:
    @staticmethod
    def initialize_db() -> oracledb.ConnectionPool:
        try:
            secret_dict = SecretManager.get_value(os.getenv("AWS_SECRETS_ORACLE"))                    
            db_user = secret_dict["username"]
            db_password = secret_dict["password"]
            db_host = str(secret_dict["host"]).split(":")[0]
            db_port = str(secret_dict["host"]).split(":")[1]
            db_sid = secret_dict["dbname"]

            oracledb.init_oracle_client()
            dsn = oracledb.makedsn(db_host, db_port, sid=db_sid)
            pool = oracledb.create_pool(
                user=db_user, password=db_password, dsn=dsn, min=1, max=10, timeout=10
            )
            initialize.log.write_log("Session pool created successfully")
            return pool
        except Exception as err:
            initialize.log.write_log(err)
            raise err
