from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from app.models import (
    User,
    Inventory,
    Stats,
    TrainingProgress
)
from app.schemas import WorldNames


fake = Faker()


def generate_unique_username(used_usernames):
    while True:
        username = fake.user_name()
        if username not in used_usernames:
            used_usernames.add(username)
            return username


async def create_users_with_related_entities(session: AsyncSession, count: int):
    users = []
    used_usernames = set()
    guest_account = fake.boolean(chance_of_getting_true=20)

    for _ in range(count):
        username = generate_unique_username(used_usernames)
        user = User(
            is_admin=False,
            username=username,
            password=fake.password(),
            email=None if guest_account else f'{username}@lazyextraction.com',
            guest_account=guest_account,
            job=fake.job(),
            training=fake.random_element(["Basic", "Advanced", "Expert"]),
            in_raid=fake.boolean(chance_of_getting_true=10),
            actions_left=fake.random_int(0, 10),
            current_world=fake.random_element(list(WorldNames)),
            current_room_data={}
        )

        inventory = Inventory(
            bank=fake.random_int(1000, 100000),
            energy=fake.random_int(0, 100),
            current_weight=0.0,
            user=user
        )
        stats = Stats(
            level=fake.pyfloat(min_value=1, max_value=50, right_digits=2),
            reputation=fake.pyfloat(min_value=1, max_value=1000, right_digits=2),
            max_energy=fake.random_int(100, 200),
            luck=fake.pyfloat(min_value=1, max_value=10, right_digits=2),
            knowledge=fake.pyfloat(min_value=1, max_value=10, right_digits=2),
            max_weight=fake.pyfloat(min_value=100, max_value=500, right_digits=2),
            agility=fake.pyfloat(min_value=1, max_value=10, right_digits=2),
            health=fake.random_int(50, 150),
            damage=fake.random_int(0, 50),
            strength=fake.pyfloat(min_value=1, max_value=10, right_digits=2),
            head_protection=fake.random_int(1, 10),
            chest_protection=fake.random_int(1, 10),
            stomach_protection=fake.random_int(1, 10),
            arm_protection=fake.random_int(1, 10),
            user=user
        )
        training_progress = TrainingProgress(
            basic_training=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            advanced_infantry=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            special_operations=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            intelligence=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            engineering=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            medical=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            leadership=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            economics=fake.pyfloat(min_value=0, max_value=200, right_digits=2),
            user=user
        )

        session.add_all([user, inventory, stats, training_progress])
        users.append(user)

    await session.flush()
    return users

