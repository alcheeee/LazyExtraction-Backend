from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.corporation_schema import NewCorporationInfo, CorporationDefaults
from ...crud.corp_crud import CorporationCRUD
from ...crud.user_crud import UserCRUD
from ...models import (
    User,
    Corporation,
    CorporationItems
)



class CorporationHandler:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.corp_crud = CorporationCRUD(Corporation, session=session)
        self.user_crud = UserCRUD(User, session=session)

    async def before_create_checks(self, corp_name: str, user_id: int) -> ValueError or None:
        """
        Create Corporation Checks
        """
        existing_corporation = await self.corp_crud.check_existing_corporation_name(corp_name)
        if existing_corporation:
            raise ValueError("A corporation with that name already exists.")

        user_in_corp = await self.user_crud.get_user_field_from_id(user_id, 'corp_id')
        if user_in_corp:
            raise ValueError("You must leave your current corporation first!")


    async def create_corporation(self, new_corp_data: NewCorporationInfo, user_id: int) -> Corporation:
        """
        Main function for creating a Corporation
        """
        await self.before_create_checks(new_corp_data.name, user_id)
        new_corporation = await self.prepare_new_corporation(new_corp_data, user_id)
        defaults = CorporationDefaults.get_defaults(new_corp_data.type)
        for item_type in defaults['items']:
            new_item = CorporationItems(item_name=item_type.value, corporation=new_corporation)
            self.session.add(new_item)
        return new_corporation

    async def prepare_new_corporation(self, new_corp_data: NewCorporationInfo, user_id: int):
        """
        Prepare transaction for a new corporation
        """
        new_corporation = Corporation(
            name=new_corp_data.name,
            type=new_corp_data.type,
            leader=await self.user_crud.get_user_field_from_id(user_id, 'username')
        )
        self.session.add(new_corporation)
        return new_corporation

    async def remove_corporation(self, corp_id: int):
        result = await self.corp_crud.delete_corporation(corp_id)
        if result.rowcount != 1:
            raise Exception("Error removing Corporation, value count not 1")
        return "Successfully removed Corporation"

    async def add_user_to_corporation(self, user_id: int, corp_id: int):
        user_corp = await self.user_crud.get_user_field_from_id(user_id, 'corp_id')
        if user_corp:
            raise ValueError("They are already in a corporation.")
        await self.user_crud.change_user_corp_id(user_id, corp_id)
        return "Successfully added to the corporation"

    async def check_if_user_is_leader(self, leader_id: int, corporation_id: int):
        assumed_leader_username = await self.user_crud.get_user_field_from_id(leader_id, 'username')
        actual_leader_username = await self.corp_crud.get_corporation_leader(corporation_id)
        if assumed_leader_username != actual_leader_username:
            raise ValueError("You do not have permissions to perform this action")

    async def remove_player_from_corporation(self, user_id: int, corp_id: int):
        user_corp_id = await self.user_crud.get_user_field_from_id(user_id, 'corp_id')
        if user_corp_id != corp_id:
            raise ValueError("That person is not part of the Corporation")
        remove_user = await self.user_crud.change_user_corp_id(user_id)
        return "Successfully removed the player from Corporation"








