import pytest
from . import Check, second_user


class TestCrews:
    """
    Tests different Crew functionality
    """

    def test_create_crew(self, client, test_user):
        data = {
            'name': 'test-crew',
            'private': False
        }
        response = client.post("/crews/create-crew", json=data, headers=test_user.headers)
        Check.valid_request(response)
        assert response.json().get("message") == "test-crew created successfully!"

    @pytest.mark.parametrize(
        "crew_input, expected_status_code, headers",
        [
            # Missing field
            ({'name': None, 'private': False}, 422, second_user.headers),
            # Same name
            ({'name': 'test-crew', 'private': False}, 400, second_user.headers),
            # Successful creation
            ({'name': 'test-crew-2', 'private': False}, 200, second_user.headers),
        ]
    )
    def test_create_crew_fails(self, client, crew_input, expected_status_code, headers):
        response = client.post("/crews/create-crew", json=crew_input, headers=headers)
        assert response.status_code == expected_status_code
        if crew_input.get('name') == 'test-crew-2':
            Check.valid_request(response)


    def _test_invite_to_crew(self, client, test_user):
        ...  # Has to be adjusted in backend to use username and not id
