from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import (
    UserCRUD,
    WorldCRUD,
    UserInventoryCRUD,
    ItemsCRUD
)


class GetUserInfo:

    def __init__(self, user_id: int, session: AsyncSession):
        self.session = session


    async def get_user_stats(self):
        pass


    async def get_user_inventory(self):
        pass


