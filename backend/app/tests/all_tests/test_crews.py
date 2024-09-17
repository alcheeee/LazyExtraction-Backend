import pytest
from . import Check, user, second_user


class TestCrews:
    """
    Tests different Crew functionality
    """

    @pytest.mark.parametrize(
        "crew_input, expected_status_code, headers",
        [
            # Not Authenticated
            ({'name': 'test-crew', 'private': False}, 403, None),
            # Successful creation
            ({'name': 'test-crew', 'private': False}, 200, user.headers),
            # Missing field
            ({'name': None, 'private': False}, 422, second_user.headers),
            # Same name
            ({'name': 'test-crew', 'private': False}, 400, second_user.headers),
            # User is already in a crew
            ({'name': 'already-leader', 'private': False}, 400, user.headers)
        ]
    )
    def test_create_crew(self, client, crew_input, expected_status_code, headers):
        response = client.post("/crews/create-crew", json=crew_input, headers=headers)
        assert response.status_code == expected_status_code

        if crew_input['name'] == 'test-crew' and response.status_code == 200:
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'success'
            assert response.json().get("message") == "test-crew created successfully!"


    @pytest.mark.parametrize(
        "add_user_input, expected_status_code, headers",
        [
            # Not Authenticated
            ({'user_to_add_remove': second_user.username, 'crew_id': 1}, 403, None),
            # Successful addition
            ({'user_to_add_remove': second_user.username, 'crew_id': 1}, 200, user.headers),
            # Adding yourself
            ({'user_to_add_remove': user.username, 'crew_id': 1}, 400, user.headers),
            # User already in a crew
            ({'user_to_add_remove': second_user.username, 'crew_id': 1}, 400, user.headers),
            # Non-existing user
            ({'user_to_add_remove': '___', 'crew_id': 1}, 400, user.headers)
        ]
    )
    def test_add_user_to_crew(self, client, add_user_input, expected_status_code, headers):
        response = client.post("/crews/add-user", json=add_user_input, headers=headers)
        assert response.status_code == expected_status_code

        if response.status_code == 200:
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'success'
            assert response.json().get("message") == "Successfully added to the crew"


    @pytest.mark.parametrize(
        "remove_user_input, expected_status_code, headers",
        [
            # Not Authenticated
            ({'user_to_add_remove': user.username, 'crew_id': 1}, 403, None),
            # Member tries removing leader
            ({'user_to_add_remove': user.username, 'crew_id': 1}, 400, second_user.headers),
            # Successful removal
            ({'user_to_add_remove': second_user.username, 'crew_id': 1}, 200, user.headers),
            # Removing yourself
            ({'user_to_add_remove': user.username, 'crew_id': 1}, 400, user.headers),
            # User not in the crew
            ({'user_to_add_remove': second_user.username, 'crew_id': 1}, 400, user.headers),
            # Non-existing user
            ({'user_to_add_remove': '___', 'crew_id': 1}, 400, user.headers)
        ]
    )
    def test_remove_user_from_crew(self, client, remove_user_input, expected_status_code, headers):
        response = client.post("/crews/remove-user", json=remove_user_input, headers=headers)
        assert response.status_code == expected_status_code

        if response.status_code == 200:
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'success'
            assert response.json().get("message") == "Successfully removed the player from Crew"
