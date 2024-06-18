import json
import time
from django.conf import settings
import requests


class AmocrmAPI:
    def __init__(
            self,
            subdomain: str,
            client_id: str,
            client_secret: str,
            code: str,
            redirect_uri: str,
            token_filename: str
    ) -> None:
        self.subdomain = subdomain
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri
        self.token_filename = token_filename
        self.base_url = f"https://{self.subdomain}.amocrm.ru/"
        self.api_url = f"{self.base_url}api/v4/"

    def _save_token_data(self, data):
        url = f"{self.base_url}oauth2/access_token"
        response = requests.post(url, json=data).json()
        data = {
            "access_token": response['access_token'],
            "refresh_token": response['refresh_token'],
            "token_type": response['token_type'],
            "expires_in": response['expires_in'],
            "end_token_time": response['expires_in'] + time.time(),
        }
        with open(settings.BASE_DIR / self.token_filename, 'w') as outfile:
            json.dump(data, outfile)
        return data["access_token"]

    def _auth(self):
        return self._save_token_data({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': self.redirect_uri,
        })

    def _update_access_token(self, refresh_token: str):
        return self._save_token_data({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'redirect_uri': self.redirect_uri,
            "refresh_token": refresh_token,
        })

    def _get_access_token(self):
        with open(settings.BASE_DIR / self.token_filename) as json_file:
            token_info = json.load(json_file)
            if token_info["end_token_time"] - 60 < time.time():
                return self._update_access_token(token_info["refresh_token"])
            else:
                return dict(token_info)["access_token"]

    def post_request(self, url: str, body: list[dict[str, str]]):
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
        }
        return requests.post(url=f"{self.api_url}{url}", headers=headers, json=body)

    def get_request(self, url: str):
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
        }
        return requests.get(url=f"{self.api_url}{url}", headers=headers)
