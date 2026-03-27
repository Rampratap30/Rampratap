import json
import os

import boto3
from botocore.exceptions import ClientError


class awsS3Upload:
    @staticmethod
    def s3_upload(file):
        try:
            region = os.getenv("AWS_REGION")
            bucket = os.getenv("AWS_S3_BUCKET")
            bucket_key = os.getenv("AWS_S3_BUCKET_KEY")
            serviceName = "s3"

            try:
                s3_client = boto3.client(service_name=serviceName)
                s3_client.upload_fileobj(file, bucket, bucket_key + file.filename)
            except ClientError as error:
                print(f"Error {error}.")
                raise error
        except Exception as err:
            err.args += tuple(["Error in S3"])
            raise err
