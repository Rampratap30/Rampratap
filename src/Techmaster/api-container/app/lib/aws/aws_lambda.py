import json
import os

import boto3
from botocore.exceptions import ClientError


class awsLambda:
    @staticmethod
    def invoke_function(lambdaName: str, function_params: dict, get_log: bool = False):
        try:
            region = os.getenv("AWS_REGION")
            serviceName = "lambda"

            try:
                lambda_client = boto3.client(
                    service_name=serviceName, region_name=region
                )
                response = lambda_client.invoke(
                    FunctionName=lambdaName,
                    InvocationType='Event',
                    Payload=json.dumps(function_params),
                    LogType="Tail" if get_log else "None",
                )
                return response
            except ClientError as error:
                print(f"Error {error}.")
                raise
        except Exception as err:
            err.args += tuple(["Error in Lambda invoke"])
            raise err
