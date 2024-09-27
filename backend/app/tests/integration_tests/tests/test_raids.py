import pytest
from app.tests.response import Check
from app.tests.helper_functions import check_item_in_inventory, get_user_inventory_items




class TestRaids:
    """
    Multitude of room tests, will consistently need adjustment as this is a new feature
    """

    @pytest.mark.parametrize(
        "raid_input, expected_status_code, headers",
        [
            # Not Authenticated
            ('Forest', 403, None),
            # Non-Existent World
            ('InvalidWorld', 422, user.headers),
            # Missing field
            (None, 422, user.headers),
            # Correct World
            ('Forest', 200, user.headers)
        ]
    )
    def test_enter_raid(self, client, raid_input, expected_status_code, headers, test_user):
        response = client.post(f"/game/new-world?request={raid_input}", headers=headers)
        assert response.status_code == expected_status_code

        if response.status_code == 200:
            json_data = Check.valid_room_data(response)
            assert json_data['message'] == "Entered a raid"
            test_user.raid.set_in_raid(True, json_data=json_data)


    @pytest.mark.parametrize(
        "interaction_option, expected_status_code, headers",
        [
            # Not authenticated
            ({'action': 'extract', 'id': 0}, 403, None),
            # Extract too early, 20 actions required
            ({'action': 'extract', 'id': 0}, 400, user.headers),
            # Item not in room
            ({'action': 'pickup', 'id': 1000}, 400, user.headers),
            # Null value
            ({'action': None, 'id': 0}, 422, user.headers)
        ]
    )
    def test_raid_interaction_fails(self, client, interaction_option, expected_status_code, headers):
        response = client.post("/game/interaction", json=interaction_option, headers=headers)
        assert response.status_code == expected_status_code


    def test_raid_pickup(self, client, test_user):
        item_id = test_user.raid.pop_raid_item_id()
        data = {
            'action': 'pickup',
            'id': int(item_id)
        }

        response = client.post("/game/interaction", json=data, headers=test_user.headers)
        assert response.status_code == 200

        item_data: dict = response.json()['room-data']['picked-up']
        assert item_data is not None
        test_user.inventory.item_picked_up(item_data)

        inventory_data = get_user_inventory_items(client, test_user)
        item_found = check_item_in_inventory(
            inventory_data,
            inventory_item_id=item_data['inv_item']['id'],
            expected_inventory=1,
            expected_stash=0
        )
        assert item_found is True


    def test_raid_extract(self, client, test_user):
        import time
        while test_user.raid.interaction_count < 20:
            # Traverse or pickup for interaction counter
            action_id = test_user.raid.pop_raid_item_id()
            action = 'pickup' if action_id else 'traverse'
            if action_id is None:
                action_id = test_user.raid.pop_connection()

            data = {
                'action': action,
                'id': int(action_id)
            }
            response = client.post("/game/interaction", json=data, headers=test_user.headers)
            assert response.status_code == 200

            if action == 'traverse':
                json_data = Check.valid_room_data(response)
                assert json_data['message'] == "Entered a new room"
                test_user.raid.set_in_raid(True, json_data=json_data)

            elif action == 'pickup':
                item_data: dict = response.json()['room-data']['picked-up']
                assert item_data is not None
                test_user.inventory.item_picked_up(item_data)

        data = {
            'action': 'extract',
            'id': 0
        }
        response = client.post("/game/interaction", json=data, headers=test_user.headers)
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        assert response.json()['message'] == "Successfully Extracted!"

