import uuid

all_item_ids = {
    '9bdd9222-8028-4e7b-a9fa-ef1a83956a4a': 'Apple'
}
def generate_id(all_item_ids: dict, item_name: str):
    all_item_ids[str(uuid.uuid4())] = item_name
    return all_item_ids
print(generate_id(all_item_ids, 'Apple'))