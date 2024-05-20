from sqlalchemy import select
from . import get_session
from ..crud.base_crud import BaseCRUD
from ..auth.auth_deps import password_security
from ..schemas.item_schema import equipment_map
from ..models import (
    User,
    Stats,
    Items,
    Inventory,
    InventoryItem,
    EducationProgress
)

from ..utils.logger import MyLogger
game_log = MyLogger.game()


class UserHandler:
    def __init__(self, session):
        self.session = session

    async def create_user(self, username: str, password: str, email: str):
        try:
            hashed_password = await password_security.hash_password(password=password)
            new_user = User(username=username, password=hashed_password, email=email)
            new_stats = Stats(user=new_user)
            new_inventory = Inventory(user=new_user)
            new_education = EducationProgress(user=new_user)

            self.session.add_all([new_user, new_stats, new_inventory])
            await self.session.commit()
            return f"Account created, welcome {username}!"
        except Exception as e:
            raise e


    async def adjust_energy(self, user_id: int, energy_delta: int):
        try:
            user = await self.session.get(User, user_id)
            if not user:
                raise Exception("User not found")
            if not user.inventory or not user.stats:
                raise Exception("User inventory or stats missing")
            new_energy = user.inventory.energy + energy_delta
            if new_energy < 0:
                raise ValueError("Not Enough Energy!")
            if new_energy > user.stats.max_energy:
                user.inventory.energy = user.stats.max_energy
            else:
                user.inventory.energy = new_energy
            await self.session.commit()
            return str(user.inventory.energy)
        except ValueError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            raise e


    async def update_user_inventory(self, user_id: int, item_id: int, quantity: int = 1, selling=False):
        user = await self.session.execute(select(User).where(User.id == user_id))
        user = user.scalars().first()
        if user:
            user = await self.session.merge(user)

        self.session.scalars(select(Items).where(Items.id == item_id).limit(1)).first()

        if item:
            item = await self.session.merge(item)

        item = await self.session.get(Items, item_id)
        if not user or not item:
            raise ValueError(f"Couldn't add {item_id} to {user_id}")

        # Get users inventory
        inventory_item = (await self.session.execute(
            select(InventoryItem).where(
                InventoryItem.inventory_id == user.inventory.id,
                InventoryItem.item_id == item.id
            )
        )).scalars().first()

        if not inventory_item and not selling:
            if quantity <= 0:
                raise ValueError("Cannot add zero or negative quantity.")
            inventory_item = InventoryItem(
                inventory_id=user.inventory.id,
                item_id=item.id,
                quantity=quantity
            )
            self.session.add(inventory_item)
        else:
            if selling:
                equipped_item_ids = [getattr(user.inventory, slot) for slot in equipment_map.values()]
                if item.id in equipped_item_ids and inventory_item.quantity <= quantity:
                    raise ValueError("Cannot sell an equipped item.")
                new_quantity = inventory_item.quantity - quantity
            else:
                new_quantity = inventory_item.quantity + quantity

            # Update inventory quantity
            if new_quantity < 0:
                raise ValueError("Not enough items in inventory to remove.")

            if selling and new_quantity < 1 and item.id in equipped_item_ids:
                raise ValueError("Cannot sell all equipped items")
            inventory_item.quantity = new_quantity

        action = "Added" if quantity > 0 else "Removed"
        game_log.info(f"{action} {abs(quantity)} of {item.item_name} to/from {user.username}'s inventory.")
        return action