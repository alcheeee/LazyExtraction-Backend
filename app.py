from sqlmodel import Session
from db import create_db_and_tables, engine
from UserDataManager import CreateUser, UpdateStats
import random

def test_database(amount_tests):
    for i in range(1, amount_tests):
        CreateUser(f'Dev{random.randint(100,10000)}', '123', f'dev{random.randint(100,10000)}@dev.com')

def main():
    create_db_and_tables()
    #test_database(10)
    #UpdateStats(user_id=8, stat_name='health', new_value=150)

if __name__ == "__main__":
    main()