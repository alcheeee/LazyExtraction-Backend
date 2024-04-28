from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.models import User, Stats, Inventory, InventoryItem
from ..models.item_models import Items
from ..database.CRUD.BaseCRUD import EnhancedCRUD
from .db import get_session
import bcrypt
from ..utils.logger import MyLogger
from ..game_systems.gameplay_options import default_stats_data, default_inventory_data, equipment_map
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()

class UserService:
    def __init__(self, session):
        self.session = session
        self.user_crud = EnhancedCRUD(User, session)

    async def get_user_by_id(self, user_id: int):
        """Fetch a user by their ID using CRUD operations."""
        return await self.user_crud.get_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """Fetch a user by their username using explicit query."""
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()


class UserHandler:

    async def create_user(self, username: str, password: str, email: str):
        async with get_session() as session:
            try:
                #Check for name  & email availability
                existing_user = (await session.execute(
                    select(User).where((User.username == username) | (User.email == email))
                )).scalars().first()

                if existing_user:
                    user_log.warning(f"Username {username} or email {email} already exists.")
                    return False, "Username or email already exists."

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                new_user = User(username=username, password=hashed_password, email=email)
                new_user.stats = Stats(**default_stats_data)
                new_user.inventory = Inventory(**default_inventory_data)
                session.add(new_user)
                await session.commit()
                admin_log.info(f"Created User: {new_user.username}")
                return True, f"Account created, welcome {username}!"

            except Exception as e:
                await session.rollback()
                admin_log.error(f"Failed to create user {username}: {str(e)}")
                raise


    async def adjust_energy(self, user_id: int, energy_delta: int):
        async with get_session() as session:
            try:
                user = await session.get(User, user_id)
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

                await session.commit()
                game_log.info(f"User {user.id}: Energy Adjusted by {energy_delta}. New Energy: {user.inventory.energy}.")
                return str(user.inventory.energy)

            except ValueError as e:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                admin_log.error(f"Error adjusting energy for user {user_id}: {str(e)}")
                raise


    async def update_user_inventory(self, user_id: int, item_id: int, quantity: int = 1, selling=False, session=None):
        try:
            user = await session.execute(select(User).where(User.id == user_id))
            user = user.scalars().first()
            if user:
                user = await session.merge(user)

            item = await session.execute(select(Items).where(Items.id == item_id))
            item = item.scalars().first()
            if item:
                item = await session.merge(item)

            item = await session.get(Items, item_id)
            if not user or not item:
                raise ValueError(f"Couldn't add {item_id} to {user_id}")

            # Get users inventory
            inventory_item = (await session.execute(
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
                session.add(inventory_item)
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

            await session.commit()
            action = "Added" if quantity > 0 else "Removed"
            game_log.info(f"{action} {abs(quantity)} of {item.item_name} to/from {user.username}'s inventory.")
            return action
        except ValueError as e:
            raise
        except Exception as e:
            raise

user_crud = UserHandler()