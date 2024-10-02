from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from app.models import Crew


fake = Faker()


def generate_unique_crew(used_names):
    while True:
        name = fake.company()
        if name not in used_names:
            used_names.add(name)
            return name

async def create_crews(session: AsyncSession, count: int):
    crews = []
    used_names = set()
    for _ in range(count):
        crew_name = generate_unique_crew(used_names)
        crew = Crew(
            name=crew_name,
            leader=fake.name(),
            private=fake.boolean(),
            capital=fake.random_int(1000, 1000000),
            reputation=fake.random_int(0, 1000),
            box_timer=fake.random_int(60, 1440),
            better_box=fake.random_int(0, 5),
            max_players=fake.random_int(5, 50),
            current_activity=fake.random_element([None, "Raid", "Training"]),
            activity_progress=fake.random_int(0, 100)
        )
        session.add(crew)
        crews.append(crew)

    await session.flush()
    return crews


async def assign_users_to_crews(session: AsyncSession, users, crews):
    for user in users:
        if fake.boolean(chance_of_getting_true=80):
            crew = fake.random_element(crews)
            user.crew = crew
    await session.flush()
