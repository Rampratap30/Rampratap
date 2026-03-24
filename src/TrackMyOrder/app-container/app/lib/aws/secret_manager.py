import json
import os

import boto3
from botocore.exceptions import ClientError


class SecretManager:
    @staticmethod
    def get_value(secret_id):
        try:
            region = os.getenv("AWS_REGION")
            service_name = "secretsmanager"
            if secret_id is None:
                raise ValueError("secretsmanager: Data not found.")
            try:
                secretsmanager_client = boto3.client(
                    service_name=service_name, region_name=region
                )
                kwargs = {"SecretId": secret_id}
                response = secretsmanager_client.get_secret_value(**kwargs)
                return json.loads(response["SecretString"])
            except ClientError as error:
                print(f"Error {error}.")
                raise
        except Exception as err:
            err.args += tuple(["Error in secret manager --> get_value"])
            raise err
