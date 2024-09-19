import pytest
from . import Check, user, second_user
from ..helper_functions import (
    check_item_in_inventory,
    get_user_inventory_items,
    check_bank,
    get_market_items
)
from ...game_systems.items.items_data.all_armor import armor_classes


class TestMarket:
    """
    Market Tests, adding items, removing items, buying items
    """


    def test_market_posting(self, client, test_user):
        provided_item = test_user.inventory.get_admin_provided_item()

        posting_data = {
            "inventory_item_id": provided_item['id'],
            "transaction_type": "posting",
            "item_cost": 100,
            "amount": 1
        }

        response = client.post(
            "/market/market-transaction",
            json=posting_data,
            headers=test_user.headers
        )
        assert response.status_code == 200

        updated_inventory = get_user_inventory_items(client, test_user)
        item_found = check_item_in_inventory(
            updated_inventory,
            inventory_item_id=provided_item['id'],
            expected_inventory=0,
            expected_stash=0
        )
        assert item_found is False


    def test_cancel_market_posting(self, client, test_user):
        provided_item = test_user.inventory.get_admin_provided_item()

        market_items = get_market_items(client, test_user, provided_item['item_name'])
        market_item_id = market_items[0]['id']

        cancel_data = {
            "market_item_id": market_item_id,
            "transaction_type": "cancel",
            "item_cost": 0,
            "amount": 1
        }

        response = client.post(
            "/market/market-transaction",
            json=cancel_data,
            headers=test_user.headers
        )
        assert response.status_code == 200

        updated_inventory = get_user_inventory_items(client, test_user)
        item_found = check_item_in_inventory(
            updated_inventory,
            inventory_item_id=response.json()['data']['inventory-item']['id'],
            expected_inventory=0,
            expected_stash=1
        )
        assert item_found is True

    def test_buy_item(self, client, test_user, admin_headers):
        provided_item = test_user.inventory.get_admin_provided_item()

        posting_data = {
            "inventory_item_id": provided_item['item_id'],  # Since Admin always gets this item first
            "transaction_type": "posting",
            "item_cost": 100,
            "amount": 1
        }

        response = client.post(
            "/market/market-transaction",
            json=posting_data,
            headers=admin_headers
        )
        assert response.status_code == 200

        buying_data = {
            "market_item_id": response.json()['data']['market-item']['id'],
            "transaction_type": "buying",
            "item_cost": 0,
            "amount": 1
        }

        response = client.post(
            "/market/market-transaction",
            json=buying_data,
            headers=test_user.headers
        )
        assert response.status_code == 200
        response_data = response.json()['data']
        assert response_data is not None
        assert response_data['market-item'] is not None
        assert response_data['inventory-item'] is not None


        inventory_item = response_data['inventory-item']
        market_item = response_data['market-item']
        test_user.inventory.main_inventory_data['bank'] -= market_item['item_cost']
        test_user.inventory.temp_data = inventory_item

    def test_inventory_and_bank_updated(self, client, test_user):
        temp_item = test_user.inventory.temp_data

        inventory_data = get_user_inventory_items(client, test_user)
        item_found = check_item_in_inventory(
            inventory_data,
            inventory_item_id=temp_item['id'],
            expected_inventory=0,
            expected_stash=2
        )
        assert item_found is True

        bank_matches = check_bank(client, test_user, test_user.inventory.main_inventory_data['bank'])
        assert bank_matches is True

    def test_quick_sell(self, client, test_user):
        temp_item = test_user.inventory.temp_data
        quick_sell_data = {
            "inventory_item_id": temp_item['id'],
            "transaction_type": "quick_sell",
            "item_cost": 0,
            "amount": 1
        }
        response = client.post(
            "/market/market-transaction",
            json=quick_sell_data,
            headers=test_user.headers
        )
        assert response.status_code == 200

        # This is kind of sloppy, but works for quick interactions right now
        item_value = temp_item['quick_sell_value']
        expected_bank = test_user.inventory.main_inventory_data['bank'] + item_value

        bank_matches = check_bank(client, test_user, expected_bank)
        assert bank_matches is True


    @pytest.mark.parametrize(
        "buying_data, expected_status_code, headers",
        [
            # Trying to buy own item
            ({"market_item_id": 1, "transaction_type": "buying", "item_cost": 100, "amount": 1},
             400, user.headers),

            # Not authenticated
            ({"market_item_id": 1, "transaction_type": "buying", "item_cost": 100, "amount": 1},
             403, None),

            # Buying with insufficient funds
            ({"market_item_id": 2, "transaction_type": "buying", "item_cost": 10000, "amount": 1},
             400, user.headers),

            # Buying invalid item
            ({"market_item_id": 9999, "transaction_type": "buying", "item_cost": 100, "amount": 1},
             400, user.headers),

            # Buying an item with 0 quantity
            ({"market_item_id": 1, "transaction_type": "buying", "item_cost": 100, "amount": 0},
             400, user.headers),
        ]
    )
    def test_buying_own_item_fails(self, client, buying_data, expected_status_code, headers):
        response = client.post(
            "/market/market-transaction",
            json=buying_data,
            headers=headers
        )
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize(
        "posting_data, expected_status_code, headers",
        [
            # Not authenticated
            ({"inventory_item_id": 1, "transaction_type": "posting", "item_cost": 100, "amount": 1},
             403, None),

            # Posting non-existent item
            ({"inventory_item_id": 9999, "transaction_type": "posting", "item_cost": 100, "amount": 1},
             404, user.headers),

            # Posting with 0 amount
            ({"inventory_item_id": 1, "transaction_type": "posting", "item_cost": 100, "amount": 0},
             400, user.headers),

            # Posting with negative amount
            ({"inventory_item_id": 1, "transaction_type": "posting", "item_cost": 100, "amount": -1},
             400, user.headers),

            # Posting with invalid cost
            ({"inventory_item_id": 1, "transaction_type": "posting", "item_cost": -100, "amount": 1},
             400, user.headers),
        ]
    )
    def test_market_posting_fails(self, client, posting_data, expected_status_code, headers):
        response = client.post(
            "/market/market-transaction",
            json=posting_data,
            headers=headers
        )
        assert response.status_code == expected_status_code


    @pytest.mark.parametrize(
        "cancel_data, expected_status_code, headers",
        [
            # Not authenticated
            ({"market_item_id": 1, "transaction_type": "cancel", "item_cost": 0, "amount": 1},
             403, None),

            # Canceling non-existent posting
            ({"market_item_id": 9999, "transaction_type": "cancel", "item_cost": 0, "amount": 1},
             400, user.headers),

            # Canceling someone else's posting
            ({"market_item_id": 1, "transaction_type": "cancel", "item_cost": 0, "amount": 1},
             400, user.headers),
        ]
    )
    def test_cancel_market_posting_fails(self, client, cancel_data, expected_status_code, headers):
        response = client.post(
            "/market/market-transaction",
            json=cancel_data,
            headers=headers
        )
        assert response.status_code == expected_status_code


    def test_mass_market_post(self, client, test_user):
        # TODO : Fix this mess of a function
        import time
        inventory_data = get_user_inventory_items(client, test_user)

        for item_details in inventory_data:
            amount = item_details['amount_in_inventory']
            used_inventory = True

            if item_details['amount_in_stash'] > 0:
                amount = item_details['amount_in_stash']
                used_inventory = False

            posting_data = {
                "inventory_item_id": item_details['id'],
                "transaction_type": "posting",
                "item_cost": 100,
                "amount": amount
            }

            response = client.post(
                "/market/market-transaction",
                json=posting_data,
                headers=test_user.headers
            )
            assert response.status_code == 200
            assert response.json()['data']['market-item']

            test_user.posted_items.append(response.json()['data']['market-item'])
            # Ensure item was deleted or correctly adjusted
            updated_inventory_data = get_user_inventory_items(client, test_user)

            if (item_details['amount_in_inventory'] - amount) <= 0 and (
                    item_details['amount_in_stash'] - amount) <= 0:

                item_found = check_item_in_inventory(
                    updated_inventory_data,
                    inventory_item_id=item_details['id'],
                    expected_inventory=0,
                    expected_stash=0
                )
                assert item_found is False

            elif used_inventory:
                item_found = check_item_in_inventory(
                    updated_inventory_data,
                    inventory_item_id=item_details['id'],
                    expected_inventory=0,
                    expected_stash=item_details['amount_in_stash']
                )
                assert item_found is True

            else:
                item_found = check_item_in_inventory(
                    updated_inventory_data,
                    inventory_item_id=item_details['id'],
                    expected_inventory=0,
                    expected_stash=item_details['amount_in_inventory']
                )
                assert item_found is True


    def test_posted_items_on_market(self, client, test_user):
        for posted_item in test_user.posted_items:
            item_name = posted_item['item_name']
            amount_posted = posted_item['item_quantity']
            market_items = get_market_items(client, test_user, item_name)

            # Ensure the item exists in the market with correct details
            item_found_in_market = False
            for market_item in market_items:
                if market_item['item_id'] == posted_item['item_id']:
                    item_found_in_market = True
                    assert market_item['item_quantity'] == amount_posted
                    assert market_item['item_cost'] == 100

            assert item_found_in_market


    def test_buy_own_item(self, client, test_user):
        market_post_id = test_user.posted_items.pop()['id']

        buying_data = {
            "market_item_id": market_post_id,
            "transaction_type": "buying",
            "item_cost": 0,
            "amount": 1
        }

        response = client.post(
            "/market/market-transaction",
            json=buying_data,
            headers=test_user.headers
        )
        assert response.status_code == 400
        assert response.json()['detail'] == "You can't buy your own items"

