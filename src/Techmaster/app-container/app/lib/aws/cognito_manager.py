import os

import requests

from app.lib.aws.secret_manager import secretManager

from datetime import datetime as dt, timedelta


class cognitoManager:
    @staticmethod
    def getToken():
        try:
            oauth_secret_id = os.getenv("AWS_SECRETS_OATH")
            oauth_secrets = secretManager.get_value(oauth_secret_id)
            auth_response = requests.post(
                url=oauth_secrets["accessTokenUrl"],
                data={
                    "grant_type": oauth_secrets["grantType"],
                    "client_id": oauth_secrets["clientID"],
                    "client_secret": oauth_secrets["clientSecret"],
                },
            )
            auth_response_json = auth_response.json()
            auth_token = auth_response_json["access_token"]
            auth_expiry= auth_response_json["expires_in"]
            expiry_time_utc = dt.utcnow() + timedelta(seconds=auth_expiry)
            return expiry_time_utc,auth_token, oauth_secrets["Api_url"]
        except Exception as err:
            err.args += tuple(["Error in cognito manager --> getToken"])
            raise err
