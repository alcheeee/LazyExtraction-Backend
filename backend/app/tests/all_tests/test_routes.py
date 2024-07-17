import pytest
from . import Check


class TestRoutes:
    """
    Make sure all routes are responding
    """
    @pytest.mark.parametrize(
        "route, expected_status_code",
        [
            # Routes
            ('user', 200),
            ('crews', 200),
            ('game', 200),
            ('market', 200),
            ('info', 200)
        ]
    )
    def test_routes(self, client, route, expected_status_code):
        response = client.get(f"/{route}")
        assert response.status_code == expected_status_code
        Check.valid_request(response)


    def test_admin_route(self, client, test_user):
        response = client.get('/admin')
        assert response.status_code == 401
