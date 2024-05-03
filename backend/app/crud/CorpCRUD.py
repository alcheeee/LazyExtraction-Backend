from sqlalchemy.orm import selectinload
from sqlalchemy import select
from .BaseCRUD import BaseCRUD
from ..models.corp_models import Corporation, CorporationItems

class CorporationCRUD(BaseCRUD):

    async def get_corporation_by_id(self, corp_id: int, load_items: bool = False):
        query = select(Corporation).where(Corporation.id == corp_id)
        if load_items:
            query = query.options(selectinload(Corporation.items))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_corporation_by_name(self, corp_name: str):
        query = select(Corporation).where(Corporation.name == corp_name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_or_update_corporation(self, corp_data: dict):
        corporation = await self.get_corporation_by_id(corp_data.get("id"))
        if corporation:
            for key, value in corp_data.items():
                setattr(corporation, key, value)
        else:
            corporation = Corporation(**corp_data)
            self.session.add(corporation)
        await self.session.commit()
        return corporation

    async def add_item_to_corporation(self, corp_id: int, item_data: dict):
        item = CorporationItems(**item_data, corporation_id=corp_id)
        self.session.add(item)
        await self.session.commit()
        return item


