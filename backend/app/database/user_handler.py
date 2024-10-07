from typing import Any
from datetime import timedelta

from fastapi.concurrency import run_in_threadpool

from app.auth.auth_deps import PasswordSecurity, TokenHandler
from app.models import (
    User,
    Stats,
    Inventory,
    TrainingProgress
)
from app.schemas.token_schema import TokenData
from app.utils.logger import MyLogger
from app.settings import settings

game_log = MyLogger.game()


class UserHandler:
    def __init__(self, session):
        self.session = session

    async def create_user(
            self, username: str, password: str, email: str,
            guest_account: bool = False, game_bot: bool = False
    ) -> dict[str, Any] | User:
        try:
            hashed_password = await run_in_threadpool(PasswordSecurity.hash_password, password)
            new_user = User(username=username, password=hashed_password, email=email, guest_account=guest_account)
            new_stats = Stats(user=new_user)
            new_inventory = Inventory(user=new_user)
            new_training = TrainingProgress(user=new_user)

            self.session.add_all([new_user, new_stats, new_inventory, new_training])
            await self.session.commit()

            if game_bot:
                return new_user

            token_data = TokenData(username=username, user_id=str(new_user.id))

            access_token, refresh_token = await run_in_threadpool(self.create_tokens, token_data)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email,
                    'guest_account': guest_account,

                },
                'inventory': new_user.inventory,
                'stats': new_user.stats,
                'trainingprogress': new_user.training_progress
            }

        except Exception as e:
            raise e

    @staticmethod
    def create_tokens(token_data: TokenData):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = TokenHandler.create_access_token(
            token_data=token_data,
            expires_delta=access_token_expires
        )
        refresh_token = TokenHandler.create_access_token(
            token_data=token_data,
            expires_delta=refresh_token_expires,
            refresh=True
        )
        return access_token, refresh_token
