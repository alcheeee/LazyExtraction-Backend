import factory
from faker import Faker
from app.models import (
    User,
    Crew,
    Inventory,
    Stats,
    TrainingProgress,
    Items,
    InventoryItem
)


fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.LazyAttribute(lambda _: fake.user_name())
    password = factory.LazyAttribute(lambda _: fake.password())
    email = factory.LazyAttribute(lambda _: fake.email())
    is_admin = False
    guest_account = False
    crew_id = None
    inventory_id = None
    stats_id = None
    training_progress_id = None


class ItemsFactory(factory.Factory):
    class Meta:
        model = Items

    id = factory.Sequence(lambda n: n)
    item_name = factory.LazyAttribute(lambda _: fake.word())
    category = "Weapon"
    tier = "Tier1"
    quick_sell = 5
    weight = 1.0
    can_be_modified = False
    allowed_modifications = None


class InventoryFactory(factory.Factory):
    class Meta:
        model = Inventory

    id = factory.Sequence(lambda n: n)


class InventoryItemFactory(factory.Factory):
    class Meta:
        model = InventoryItem

    item_name = factory.LazyAttribute(lambda obj: obj.item.item_name)
    amount_in_stash = 0
    amount_in_inventory = 1
    one_equipped = False
    is_modified = False
    quick_sell_value = 5
    modifications = {}


class StatsFactory(factory.Factory):
    class Meta:
        model = Stats

    id = factory.Sequence(lambda n: n)
    level = 1.0
    reputation = 1.0
    max_energy = 100
    agility = 1.0
    health = 100
    luck = 1.0
    max_weight = 100.0


class TrainingProgressFactory(factory.Factory):
    class Meta:
        model = TrainingProgress

    id = factory.Sequence(lambda n: n)


class CrewFactory(factory.Factory):
    class Meta:
        model = Crew

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda _: fake.company())
    leader = factory.LazyAttribute(lambda _: fake.name())
