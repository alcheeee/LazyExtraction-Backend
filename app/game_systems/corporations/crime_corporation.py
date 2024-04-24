from sqlmodel import Session, select
from app.models.models import User
from app.models.corp_models import Corporations, CorpUpgrades, CorpInventory, CorpInventoryItem, CorpChallenges
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()


class CorporationActivity:
    def __init__(self, corporation, session=Session):
        self.session = session
        self.corporation = corporation
        try:
            self.corp_stats = session.exec(select(CorpUpgrades)
                                              .where(CorpUpgrades.corporation_id == corporation.id))
        except Exception as e:
            self.corp_stats = None

    def Heist(self):
        if self.corporation.corporation_type != "Criminal":
            raise ValueError("Invalid Corporation type")

        chances_to_escape = self.corporation.corporation_type