from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from .BaseCRUD import BaseCRUD
from ..models.models import User
from ..models.corp_models import Corporation, CorporationItems

class CorporationCRUD(BaseCRUD):

    # Get Corporation by its id
    async def get_corporation_by_id(self, corp_id: int, load_items: bool = False):
        query = select(Corporation).where(Corporation.id == corp_id)
        if load_items:
            query = query.options(selectinload(Corporation.items))
        return await self.execute_scalar_one_or_none(query)

    # Get Corporation id by its name
    async def get_corporation_name_by_id(self, corp_id: int):
        query = select(Corporation.name).where(Corporation.id == corp_id)
        return await self.execute_scalar_one_or_none(query)

    # Check if Corporation name already exists
    async def check_existing_corporation_name(self, corp_name: str):
        query = select(Corporation.name).where(Corporation.name == corp_name)
        return await self.execute_scalar_one_or_none(query)

    # Gets the leader of a Corporation
    async def get_corporation_leader(self, corp_id: int):
        query = select(Corporation.leader).where(Corporation.id == corp_id)
        return await self.execute_scalar_one_or_none(query)

    # Main function for removing a Corporation from the database
    async def delete_corporation(self, corporation_id: int):
        await self.remove_all_users_from_corporation(corporation_id)
        await self.delete_corporation_items(corporation_id)
        delete_query = delete(Corporation).where(Corporation.id == corporation_id)
        result = await self.session.execute(delete_query)
        return result

    # Removes all players associated with the given corporation
    async def remove_all_users_from_corporation(self, corporation_id: int):
        update_users = update(User).where(User.corp_id == corporation_id).values(corp_id=None)
        await self.session.execute(update_users)

    # Get all current Corporation members
    async def get_all_corporation_members(self, corporation_id: int):
        all_members = select(User.id).where(User.corp_id == corporation_id)
        result = await self.session.execute(all_members)
        return [user_id[0] for user_id in result.all()]

    # Removes all items linked to a corporation
    async def delete_corporation_items(self, corporation_id: int):
        delete_items = delete(CorporationItems).where(CorporationItems.corporation_id == corporation_id)
        await self.session.execute(delete_items)

    # Adds Items to a Corporation
    async def add_item_to_corporation(self, corp_id: int, item_data: dict):
        item = CorporationItems(**item_data, corporation_id=corp_id)
        self.session.add(item)
        return item

