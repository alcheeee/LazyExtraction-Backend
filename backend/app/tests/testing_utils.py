from typing import Optional
import datetime


class UserAccount:
    def __init__(self):
        self.username: str = f"test-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.email: str = f"{self.username}@LETests.com"
        self.password: str = f"123456"
        self.auth_token: Optional[str] = None


class Check:

    @staticmethod
    def valid_login_request(response):
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data
        assert data['access_token'] is not None
        return data['access_token']


    @staticmethod
    def valid_request(response):
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'

