from .account_util import UserAccount

class Check:

    @staticmethod
    def valid_login(response, user: UserAccount):
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        user.refresh_token = data['refresh_token']
        user.auth_token = data['access_token']
        user.headers["Authorization"] = f"Bearer {data['access_token']}"

    @staticmethod
    def valid_room_data(response):
        json_data = response.json()
        assert json_data['status'] == "success"
        assert json_data['room-data']['items']
        assert json_data['room-data']['connections']
        return json_data
