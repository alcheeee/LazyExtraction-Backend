# Repeated test calls


def get_user_inventory_items(client, user):
    response = client.get(
        "/info/get-user-info?request=inventory_items",
        headers=user.headers
    )
    assert response.status_code == 200
    response_data = response.json()

    assert 'all-inventory-items' in response_data

    return response.json()['all-inventory-items']


def check_item_in_inventory(inventory_data, inventory_item_id, expected_inventory=0, expected_stash=0):
    """Check if an item is in the user's inventory."""
    for item_data in inventory_data:
        if item_data['id'] == inventory_item_id:
            assert item_data['amount_in_inventory'] == expected_inventory
            assert item_data['amount_in_stash'] == expected_stash
            return True

    return False


def check_bank(client, user, expected_value):
    response = client.get(
        '/info/get-user-info?request=inventory',
        headers=user.headers
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['user-inventory'] is not None

    bank_value = response_json['user-inventory']['bank']
    user.inventory.main_inventory_data['bank'] = bank_value
    return True if bank_value == expected_value else False


def get_market_items(client, test_user, item_name, offset=0):
    """Helper to fetch market items by name."""
    response = client.get(
        f"/market/market-items-by-name?item_name={item_name}&offset={offset}",
        headers=test_user.headers
    )
    assert response.status_code == 200
    return response.json()
