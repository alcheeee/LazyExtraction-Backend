from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from .base_crud import BaseCRUD
from app.models import (
    User,
    Crew,
    CrewItems
)


class CrewCRUD(BaseCRUD):

    # Get Crew by its id
    async def get_crew_by_id(self, crew_id: int, load_items: bool = False):
        query = select(Crew).where(Crew.id == crew_id)
        if load_items:
            query = query.options(selectinload(Crew.items))
        return await self.execute_scalar_one_or_none(query)

    # Get Crew id by its name
    async def get_crew_name_by_id(self, crew_id: int):
        query = select(Crew.name).where(Crew.id == crew_id)
        return await self.execute_scalar_one_or_none(query)

    # Check if Crew name already exists
    async def check_existing_crew_name(self, crew_name: str):
        query = select(Crew.name).where(Crew.name == crew_name)
        return await self.execute_scalar_one_or_none(query)

    # Gets the leader of a Crew
    async def get_crew_leader(self, crew_id: int):
        query = select(Crew.leader).where(Crew.id == crew_id)
        return await self.execute_scalar_one_or_none(query)

    # Main function for removing a Crew from the database
    async def delete_crew(self, crew_id: int):
        crew = await self.get_crew_by_id(crew_id)
        if not crew:
            raise LookupError("Crew not found")
        await self.remove_all_users_from_crew(crew_id)
        await self.delete_crew_items(crew_id)
        delete_query = delete(Crew).where(Crew.id == crew_id)
        result = await self.session.execute(delete_query)
        return result

    # Removes all players associated with the given crew
    async def remove_all_users_from_crew(self, crew_id: int):
        update_users = update(User).where(User.crew_id == crew_id).values(crew_id=None)
        await self.session.execute(update_users)

    # Get all current Crew members
    async def get_all_crew_members(self, crew_id: int):
        all_members = select(User.id).where(User.crew_id == crew_id)
        result = await self.session.execute(all_members)
        return [user_id[0] for user_id in result.all()]

    # Removes all items linked to a crew
    async def delete_crew_items(self, crew_id: int):
        delete_items = delete(CrewItems).where(CrewItems.crew_id == crew_id)
        await self.session.execute(delete_items)

    # Adds Items to a Crew
    async def add_item_to_crew(self, crew_id: int, item_data: dict):
        item = CrewItems(**item_data, crew_id=crew_id)
        self.session.add(item)
        return item

