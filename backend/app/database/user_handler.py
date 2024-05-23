from sqlalchemy import select
from . import get_session
from ..crud.base_crud import BaseCRUD
from ..auth.auth_deps import password_security
from ..schemas import equipment_map
from ..models import (
    User,
    Stats,
    Items,
    Inventory,
    InventoryItem,
    TrainingProgress
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
            new_training = TrainingProgress(user=new_user)

            self.session.add_all([new_user, new_stats, new_inventory, new_training])
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
