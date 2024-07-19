import pytest
from . import Check, user, second_user


class TestRaids:
    """
    Multitude of room tests, will consistently need adjustment as this is a new feature
    """

    @pytest.mark.parametrize(
        "raid_input, expected_status_code, headers",
        [
            # Not Authenticated
            ('Laboratory', 401, None),
            # Non-Existent World
            ('InvalidWorld', 422, user.headers),
            # Missing field
            (None, 422, user.headers),
            # Correct World
            ('Laboratory', 200, user.headers)
        ]
    )
    def test_enter_raid(self, client, raid_input, expected_status_code, headers):
        response = client.post(f"/game/new-world?world_name={raid_input}", headers=headers)
        assert response.status_code == expected_status_code

        if response.status_code == 200:
            json_data = response.json()
            assert json_data['status'] == "success"
            assert json_data['message'] == "Entered a raid"
            assert json_data['room-data']['items']
            assert json_data['room-data']['connections']
            user.raid.set_in_raid(True, json_data=json_data)


    @pytest.mark.parametrize(
        "interaction_option, expected_status_code, headers",
        [
            # Not authenticated
            ({'action': 'extract', 'id': 0}, 401, None),
            # Extract too early, 20 actions required
            ({'action': 'extract', 'id': 0}, 400, user.headers),
            # Item not in room
            ({'action': 'pickup', 'id': 1000}, 400, user.headers),
            # Null value
            ({'action': None, 'id': 0}, 422, user.headers)
        ]
    )
    def test_raid_interaction_fails(self, client, interaction_option, expected_status_code, headers):
        # Options: pickup, traverse, extract
        response = client.post("/game/interaction", json=interaction_option, headers=headers)
        assert response.status_code == expected_status_code


    def test_raid_pickup(self, client, test_user):
        item_id = test_user.raid.pop_raid_item_id()
        data = {
            'action': 'pickup',
            'id': item_id
        }
        response = client.post("/game/interaction", json=data, headers=test_user.headers)
        assert response.status_code == 200












