from sqlmodel import Session, select
from models import User, Stats
from db import engine

def CreateUser(username: str, password: str, email: str):
    with Session(engine) as session:
        new_user = User(username=username, password=password, email=email)
        stats_data = {
            'level': 1,
            'health': 100,
            'stamina': 100,
            'strength': 1,
            'intelligence': 1,
            'knowledge': 1}

        user_stats = Stats(**stats_data)
        new_user.stats = user_stats
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        print("Created User:", new_user)
        print("Users Stats:", new_user.stats)

def UpdateStats(user_id: int, stat_name: str, new_value: int):
    with Session(engine) as session:
        try:
            user = session.get(User, user_id)
            stats = session.get(Stats, user.stats_id)
        except:
            print(f"No user found with ID {user_id}")
            return

        if hasattr(stats, stat_name):
            setattr(stats, stat_name, new_value)
            session.add(stats)
            session.commit()

            print(f"Updated '{stat_name}' for user {user.id} to {new_value}.")
        else:
            print(f"Stat {stat_name} does not exist.")