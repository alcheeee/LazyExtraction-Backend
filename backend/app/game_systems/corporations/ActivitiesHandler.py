from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...models.models import User
from ...models.corp_models import Corporation, CorpUpgrades, CorpInventory, CorpInventoryItem, CorpActivities
from ...utils.logger import MyLogger
admin_log = MyLogger.admin()


class ActivityHandler:
    def __init__(self, corporation, session: AsyncSession):
        self.session = session
        self.corporation = corporation

    def new_activity(self, activity_name, progress_required, activity_reward=None, required_rep=None, activity_cost=None):
        new_activity = CorpActivities(activity_name=activity_name,
                                  activity_cost=activity_cost,
                                  activity_reward=activity_reward,
                                  progress_required=progress_required,
                                  required_rep=required_rep,
                                  corporation_id=self.corporation.id)
        return new_activity

    async def check_if_finished(self, activity_id: int):
        activity = await self.session.get(CorpActivities, activity_id)
        if not activity:
            raise ValueError("No activity found")

        if activity.corporation_id != self.corporation.id:
            raise ValueError("Activity does not belong to this corporation")

        if activity.progress < activity.required_progress:
            return False

        reward_parts = activity.reward.split(maxsplit=1)
        if len(reward_parts) != 2:
            raise ValueError("Invalid reward format")

        reward_type, amount = reward_parts
        try:
            amount_int = int(amount)
        except ValueError:
            raise ValueError("Invalid amount in reward")

        # DELETE ACTIVITY FROM DATABASE IN ROUTE IF SUCCESS
        if reward_type == "Capital":
            return ("Capital", self.corporation.capital + amount_int)
        elif reward_type == "Reputation":
            return ("Reputation", self.corporation.reputation + amount_int)
        elif reward_type == "Item":
            item_details = amount.split()
            if len(item_details) != 2:
                raise ValueError("Invalid item reward format")
            item_name, item_quantity = item_details[0], int(item_details[1])
            return ("Item", item_name, item_quantity)

        raise ValueError("Invalid reward type")


