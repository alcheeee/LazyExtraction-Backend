from UserDataManager import user_data_manager
from Corporations.CorporationManager import corporation_manager
from db import create_db_and_tables
import random

def add_users_to_database(amount_tests):
    for i in range(1, amount_tests):
        user_data_manager.create_user(f'Dev{random.randint(100,10000)}', '123', f'dev{random.randint(100,10000)}@dev.com')

def Tests():
    add_users_to_database(10)

    user_data_manager.update_stat(user_id=8, stat_name='health', new_value=300)
    user_data_manager.adjust_energy(user_id=3, energy_delta=-1)

    corporation_manager.create_corporation('Dev Team', 'Crime')
    corporation_manager.add_user_to_corporation(user_id=6, corporation_id=1)
    corporation_manager.add_user_to_corporation(user_id=5, corporation_id=2)


def main():
    create_db_and_tables()
    Tests()

if __name__ == "__main__":
    main()