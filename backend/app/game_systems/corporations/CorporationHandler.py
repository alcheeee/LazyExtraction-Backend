from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from ...schemas.corporation_schema import NewCorporationInfo, CorporationDefaults
from ...models.models import User
from ...crud.CorpCRUD import CorporationCRUD
from ...crud.UserCRUD import UserCRUD
from ...models.corp_models import Corporation, CorporationItems
from ...utils.logger import MyLogger
game_log = MyLogger.game()
error_log = MyLogger.errors()



class CorporationHandler:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.corp_crud = CorporationCRUD(Corporation, session=session)
        self.user_crud = UserCRUD(User, session=session)

    async def before_create_checks(self, corp_name: str, user_id: int) -> ValueError or None:
        existing_corporation = await self.corp_crud.get_corporation_by_name(corp_name)
        if existing_corporation:
            raise ValueError("A corporation with that name already exists.")

        user_in_corp = await self.user_crud.get_user_corp_id(user_id)
        if user_in_corp:
            raise ValueError("You must leave your current corporation first!")


    async def create_corporation(self, new_corp_data: NewCorporationInfo, user_id: int) -> Corporation:
        await self.before_create_checks(new_corp_data.name, user_id)
        leader_username = await self.user_crud.get_username_by_id(user_id)
        new_corporation = Corporation(
            name=new_corp_data.name,
            type=new_corp_data.type,
            leader=leader_username
        )
        self.session.add(new_corporation)
        defaults = CorporationDefaults.get_defaults(new_corp_data.type)
        for item_type in defaults['items']:
            new_item = CorporationItems(item_name=item_type.value, corporation=new_corporation)
            self.session.add(new_item)

        return new_corporation


    async def add_user_to_corporation(self, user_id: int, corporation_id: int):
        user_corp = await self.user_crud.get_user_corp_id(user_id)
        if user_corp:
            raise ValueError("They are already in a corporation.")
        update_stmt = update(User).where(User.id == user_id).values(corp_id=corporation_id)
        await self.session.execute(update_stmt)
        return "Successfully added to the corporation"


    async def remove_user_from_corporation(self, user_id: int, corporation_id: int):
        try:
            user = await self.session.get(User, user_id)
            if user is None or user.corp_id != corporation_id:
                return False, "User is not part of that corporation"

            corporation = await self.session.get(Corporation, corporation_id)
            if corporation.leader == user.username:
                return False, "Leader cannot leave the corporation"

            user.corp_id = None
            await self.session.commit()
            game_log.info(f"User {user_id} has been removed from corporation {corporation_id}.")
            return True, f"User removed from {corporation.corporation_name}"
        except Exception as e:
            await self.session.rollback()
            return False, str(e)











