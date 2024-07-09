from ..auth.auth_deps import PasswordSecurity
from ..models import (
    User,
    Stats,
    Inventory,
    TrainingProgress
)

from ..utils.logger import MyLogger
game_log = MyLogger.game()


class UserHandler:
    def __init__(self, session):
        self.session = session

    async def create_user(self, username: str, password: str, email: str):
        try:
            hashed_password = await PasswordSecurity.hash_password(password=password)
            new_user = User(username=username, password=hashed_password, email=email)
            new_stats = Stats(user=new_user)
            new_inventory = Inventory(user=new_user)
            new_training = TrainingProgress(user=new_user)

            self.session.add_all([new_user, new_stats, new_inventory, new_training])
            await self.session.commit()
            return f"Account created, welcome {username}!"
        except Exception as e:
            raise e
