import json
import os

from flask_restful import Resource, request

from app.lib.aws.aws_s3 import awsS3Upload
from app.lib.response.api_response import APIResponse
from app.lib.saml.saml_request import samlRequest

ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class fileUpload(Resource):
    method_decorators = [samlRequest.validate_auth]

    def post(self, *args, **kwargs):
        try:
            print("bulk_upload")
            uploaded_file = request.files["file"]

            if "file" not in request.files:
                error_response = [
                    {
                        "status": "Failed",
                        "message": "user_file not exists in the payload",
                    }
                ]
                return (
                    json.loads(APIResponse(errors=error_response).to_json()),
                    404,
                )
            if not allowed_file(uploaded_file.filename):
                error_response = [
                    {"status": "Failed", "message": "Invalid file format or extension."}
                ]
                return json.loads(APIResponse(errors=error_response).to_json()), 400

            output = awsS3Upload.s3_upload(uploaded_file)
            # request.post(os.getenv("LOGIN_URL")+"/api/changes/bulk_import",json=data)
            print(output)
            return (
                json.loads(
                    APIResponse(
                        data={
                            "message": "File uploaded",
                            "filename": uploaded_file.filename,
                        }
                    ).to_json()
                ),
                201,
            )

        except Exception as e:
            # Handle exceptions and return a 500 error response
            error_response = [{"status": "Failed", "message": str(e)}]
            return json.loads(APIResponse(errors=error_response).to_json()), 500
