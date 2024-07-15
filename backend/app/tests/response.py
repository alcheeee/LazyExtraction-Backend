class Check:

    @staticmethod
    def valid_request(response):
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
