class Check:

    @staticmethod
    def valid_request(response):
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'

    @staticmethod
    def valid_login(response, account):
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data
        assert data['access_token'] is not None
        account.set_auth_token(data['access_token'])
