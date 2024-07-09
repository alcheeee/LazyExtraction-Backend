from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import NewCrewInfo, CrewDefaults
from ...crud.crew_crud import CrewCRUD
from ...crud.user_crud import UserCRUD
from ...models import (
    User,
    Crew,
    CrewItems
)



class CrewHandler:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.crew_crud = CrewCRUD(Crew, session=session)
        self.user_crud = UserCRUD(User, session=session)

    async def before_create_checks(self, crew_name: str, user_id: int) -> ValueError or None:
        """
        Create Crew Checks
        """
        existing_crew = await self.crew_crud.check_existing_crew_name(crew_name)
        if existing_crew:
            raise ValueError("A crew with that name already exists.")

        user_in_crew = await self.user_crud.get_user_field_from_id(user_id, 'crew_id')
        if user_in_crew:
            raise ValueError("You must leave your current crew first!")


    async def create_crew(self, new_crew_data: NewCrewInfo, user_id: int) -> Crew:
        """
        Main function for creating a Crew
        """
        await self.before_create_checks(new_crew_data.name, user_id)
        new_crew = await self.prepare_new_crew(new_crew_data, user_id)
        for item in CrewDefaults.items:
            new_item = CrewItems(item_name=item, crew=new_crew)
            self.session.add(new_item)
        return new_crew

    async def prepare_new_crew(self, new_crew_data: NewCrewInfo, user_id: int):
        """
        Prepare transaction for a new crew
        """
        new_crew = Crew(
            name=new_crew_data.name,
            private=new_crew_data.private,
            leader=await self.user_crud.get_user_field_from_id(user_id, 'username')
        )
        self.session.add(new_crew)
        return new_crew

    async def remove_crew(self, crew_id: int):
        result = await self.crew_crud.delete_crew(crew_id)
        if result.rowcount != 1:
            raise Exception("Error removing Crew, value count not 1")
        return "Successfully removed Crew"

    async def add_user_to_crew(self, user_id: int, crew_id: int):
        user_crew = await self.user_crud.get_user_field_from_id(user_id, 'crew_id')
        if user_crew:
            raise ValueError("They are already in a crew.")
        await self.user_crud.change_user_crew_id(user_id, crew_id)
        return "Successfully added to the crew"

    async def check_if_user_is_leader(self, leader_id: int, crew_id: int):
        assumed_leader_username = await self.user_crud.get_user_field_from_id(leader_id, 'username')
        actual_leader_username = await self.crew_crud.get_crew_leader(crew_id)
        if assumed_leader_username != actual_leader_username:
            raise ValueError("You do not have permissions to perform this action")

    async def remove_player_from_crew(self, user_id: int, crew_id: int):
        user_crew_id = await self.user_crud.get_user_field_from_id(user_id, 'crew_id')
        if user_crew_id != crew_id:
            raise ValueError("That person is not part of the Crew")
        await self.user_crud.change_user_crew_id(user_id)
        return "Successfully removed the player from Crew"








