import time

import pytest
from . import Check, user, second_user
from ..helper_functions import check_item_in_inventory, get_user_inventory_items


TACTICAL_HELMET_ID = 1


class TestInventory:
    """
    Inventory Tests, switching items from stash, equipping
    Continuously changing at this point in development, will need updating
    """

    def test_get_inventory(self, client, test_user):
        response = client.get(
            "/info/get-user-info?request=inventory_items",
            headers=test_user.headers
        )
        assert response.status_code == 200
        assert response.json()['all-inventory-items']

    def test_inventory_matches_database(self, client, test_user):
        inventory_data = get_user_inventory_items(client, test_user)
        stored_inventory = test_user.inventory.inventory_data

        for item_data in inventory_data:
            stored_item = stored_inventory.get(str(item_data['item_id']))

            assert stored_item
            assert item_data['item_id'] == stored_item['item_id']
            assert item_data['id'] == stored_item['id']
            assert item_data['amount_in_inventory'] == stored_item['amount_in_inventory']
            assert item_data['amount_in_stash'] == stored_item['amount_in_stash']

    @pytest.mark.parametrize(
        "switch_input, expected_status_code, headers",
        [
            # Not Authenticated
            ({'to_stash': True, 'quantity': 1}, 403, None),
            # Remove too many
            ({'to_stash': True, 'quantity': 100}, 400, user.headers),
            # Invalid item index
            ({'to_stash': True, 'quantity': 1, 'inventory_item_id': 1000000}, 404, user.headers),
            # Move more items to stash than available in inventory
            ({'to_stash': True, 'quantity': 10}, 400, user.headers),
            # Move more items to inventory than available in stash
            ({'to_stash': False, 'quantity': 10}, 400, user.headers),
            # Negative Value
            ({'to_stash': True, 'quantity': -5}, 400, user.headers),
            # Zero quantity
            ({'to_stash': True, 'quantity': 0}, 400, user.headers),
        ]
    )
    def test_switch_item_stash_status_fails(self, client, switch_input, expected_status_code, headers):
        inventory_item_id = switch_input.get('inventory_item_id', None)
        if inventory_item_id is None:
            switch_input['inventory_item_id'] = user.inventory.get_an_item()['id']

        response = client.post(
            "/inventory/item-stash-status",
            json=switch_input,
            headers=headers
        )
        assert response.status_code == expected_status_code


    def test_switch_item_stash_status(self, client, test_user):
        item_details = user.inventory.get_an_item()
        data = {
            'to_stash': True,
            'quantity': item_details['amount_in_inventory'],
            'inventory_item_id': item_details['id']
        }

        response = client.post(
            "/inventory/item-stash-status",
            json=data,
            headers=test_user.headers
        )
        assert response.status_code == 200

        # Switch Back
        data['to_stash'] = False
        response = client.post(
            "/inventory/item-stash-status",
            json=data,
            headers=test_user.headers
        )
        assert response.status_code == 200


    def test_add_item_to_user(self, client, admin_headers):
        data = {
            'username': 'test-user',
            'item_id': TACTICAL_HELMET_ID,
            'quantity': 1
        }
        response = client.put(
            "/admin/add-item-to-user",
            json=data,
            headers=admin_headers
        )
        assert response.status_code == 200
        response_data = response.json()['data']
        user.inventory.equip_item(response_data)
        user.inventory.admin_provided_item[response_data['id']] = response_data


    def test_equip_item_from_stash(self, client, test_user):
        helmet_to_equip = test_user.inventory.get_equipped_item()
        data = {
            "inventory_item_id": helmet_to_equip['id']
        }
        response = client.post(
            f"/inventory/equip-item",
            json=data,
            headers=test_user.headers
        )
        assert response.status_code == 400

        # Switch item to Inventory
        response = client.post(
            "/inventory/item-stash-status",
            json={
                'to_stash': False,
                'quantity': 1,
                'inventory_item_id': helmet_to_equip['id']
            },
            headers=test_user.headers
        )
        assert response.status_code == 200


    def test_equip_item(self, client, test_user):
        # TODO : Equip an item for each slot category
        helmet_to_equip = test_user.inventory.get_equipped_item()
        data = {
            "inventory_item_id": helmet_to_equip['id']
        }
        response = client.post(
            f"/inventory/equip-item",
            json=data,
            headers=test_user.headers
        )
        assert response.status_code == 200


    def test_equipped_item_change_stats(self, client, test_user):
        response = client.get(
            '/info/get-user-info?request=stats',
            headers=test_user.headers
        )
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['user-stats'] is not None

        stats_data = response_json['user-stats']
        assert stats_data['head_protection'] > 1
        assert stats_data['agility'] < 1


    def test_equipped_item_inventory(self, client, test_user):
        helmet_to_equip = test_user.inventory.get_equipped_item()
        response = client.get(
            '/info/get-user-info?request=inventory',
            headers=test_user.headers
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['user-inventory'] is not None

        inventory_data = response_json['user-inventory']
        assert inventory_data['equipped_head_armor_id'] == helmet_to_equip['id']
        test_user.inventory.main_inventory_data = inventory_data


    def test_equipped_item_not_in_inventory(self, client, test_user):
        helmet_to_equip = test_user.inventory.get_equipped_item()
        inventory_data = get_user_inventory_items(client, test_user)
        item_found = check_item_in_inventory(
            inventory_data,
            inventory_item_id=helmet_to_equip['id'],
            expected_inventory=0,
            expected_stash=0
        )
        assert item_found is True


    def test_unequip_item(self, client, test_user):
        helmet_to_equip = test_user.inventory.get_equipped_item()
        data = {
            "inventory_item_id": helmet_to_equip['id']
        }
        response = client.post(
            f"/inventory/unequip-item",
            json=data,
            headers=test_user.headers
        )
        assert response.status_code == 200

        response = client.get(
            '/info/get-user-info?request=stats',
            headers=test_user.headers
        )
        assert response.status_code == 200

        response_json = response.json()
        assert response_json['user-stats'] is not None

        stats_data = response_json['user-stats']
        assert stats_data['head_protection'] == 1
        assert stats_data['agility'] == 1


    def test_unequipped_item_added_to_inv(self, client, test_user):
        helmet_to_equip = test_user.inventory.get_equipped_item()
        inventory_data = get_user_inventory_items(client, test_user)
        item_found = check_item_in_inventory(
            inventory_data,
            inventory_item_id=helmet_to_equip['id'],
            expected_inventory=1,
            expected_stash=0
        )
        assert item_found is True







