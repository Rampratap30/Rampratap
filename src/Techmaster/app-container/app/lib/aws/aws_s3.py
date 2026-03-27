import json
import os

import boto3
from botocore.exceptions import ClientError

from app.lib.aws.secret_manager import secretManager


class awsS3Upload:
    @staticmethod
    def s3_upload(file):
        try:
            region = os.getenv("AWS_REGION")
            bucket = os.getenv("AWS_S3_BUCKET")
            bucket_key = os.getenv("AWS_S3_BUCKET_KEY")
            serviceName = "s3"
            secretDit = secretManager.get_value(os.getenv("AWS_SECRETS_S3"))
            s3KeyId = secretDit["aws_access_key_id"]
            s3AccessKey = secretDit["aws_secret_access_key"]

            try:
                print(file.filename)
                s3_client = boto3.client(
                    service_name=serviceName,
                    region_name=region,
                    aws_access_key_id=s3KeyId,
                    aws_secret_access_key=s3AccessKey,
                )
                response = s3_client.upload_fileobj(
                    file, bucket, bucket_key + file.filename
                )
                return response
            except ClientError as error:
                print(f"Error {error}.")
                raise error
        except Exception as err:
            err.args += tuple(["Error in S3 - "])
            err.args += tuple([bucket])
            err.args += tuple([bucket_key])
            raise err
