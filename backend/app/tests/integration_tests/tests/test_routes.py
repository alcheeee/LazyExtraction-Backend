import pytest


class TestRoutes:
    """
    Make sure all routes are responding
    """

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "route, expected_status_code",
        [
            # Routes
            ('user', 200),
            ('crews', 200),
            ('game', 200),
            ('combat', 200),
            ('market', 200),
            ('info', 200),
            ('inventory', 200),
            ('admin', 403)
        ]
    )
    async def test_routes(self, async_client, route, expected_status_code):
        response = await async_client.get(f"/{route}/")
        assert response.status_code == expected_status_code
        if expected_status_code != 403:
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'success'
        else:
            assert response.status_code == 403

