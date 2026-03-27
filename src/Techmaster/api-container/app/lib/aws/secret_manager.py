import json
import os

import boto3
from botocore.exceptions import ClientError


class secretManager:
    @staticmethod
    def get_value(secretID):
        try:
            region = os.getenv("AWS_REGION")
            serviceName = "secretsmanager"
            if secretID is None:
                raise
            try:
                secretsmanager_client = boto3.client(
                    service_name=serviceName, region_name=region
                )
                kwargs = {"SecretId": secretID}
                response = secretsmanager_client.get_secret_value(**kwargs)
                return json.loads(response["SecretString"])
            except ClientError as error:
                print(f"Error {error}.")
                raise
        except Exception as err:
            err.args += tuple(["Error in secret manager --> get_value"])
            raise err
