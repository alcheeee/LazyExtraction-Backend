from datetime import timedelta

from ..auth.auth_deps import PasswordSecurity, TokenHandler
from ..models import (
    User,
    Stats,
    Inventory,
    TrainingProgress
)

from ..utils.logger import MyLogger
from ..config import settings
game_log = MyLogger.game()


class UserHandler:
    def __init__(self, session):
        self.session = session

    async def create_user(self, username: str, password: str, email: str,
                          guest_account: bool = False, game_bot: bool = False
    ):
        try:
            hashed_password = await PasswordSecurity.hash_password(password=password)
            new_user = User(username=username, password=hashed_password, email=email, guest_account=guest_account)
            new_stats = Stats(user=new_user)
            new_inventory = Inventory(user=new_user)
            new_training = TrainingProgress(user=new_user)

            self.session.add_all([new_user, new_stats, new_inventory, new_training])
            await self.session.commit()
            if game_bot:
                return new_user

            access_token, refresh_token = self.create_tokens(
                username,
                new_user.id
            )

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'id': new_user.id,
                'username': new_user.username,
                'guest_account': True if guest_account else False,
                'inventory': new_user.inventory,
                'stats': new_user.stats,
                'training': new_user.training_progress
            }

        except Exception as e:
            raise e

    @staticmethod
    def create_tokens(username: str, user_id: int):
        user_data = {
            "username": username,
            "user_id": str(user_id)
        }
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = TokenHandler.create_access_token(
            user_data=user_data,
            expires_delta=access_token_expires
        )
        refresh_token = TokenHandler.create_access_token(
            user_data=user_data,
            expires_delta=refresh_token_expires,
            refresh=True
        )
        return access_token, refresh_token
