#from ...schemas import WorldTier, WorldNames
from backend.app.schemas import WorldTier, WorldNames

class RoomTypes:
    def __init__(self, world_name: WorldNames, room_tier: WorldTier):
        self.world_name = world_name
        self.room_tier = room_tier


    def medical(self):
        base_items = {'Bandage': 'values'}
        if self.world_name == WorldNames.Forest:
            base_items['Pain Killer'] = 'values'

        elif self.world_name == WorldNames.Laboratory:
            base_items['Adrenaline'] = 'values'

        elif self.world_name == WorldNames.MilitaryBase:
            base_items['Medkit'] = 'values'

        return base_items


    def regular(self):
        base_items = {'Water Bottle': 'values', 'Food Ration': 'values'}

        if self.world_name == WorldNames.Forest:
            base_items['Antique'] = 'values'

        elif self.world_name == WorldNames.Laboratory:
            base_items['Jeans'] = 'values'

        return base_items


    def military(self):
        base_items = {'Ammo': 'values', 'Grenade': 'values'}

        if self.world_name == WorldNames.Forest:
            base_items['AP Slug'] = 'values'
            base_items['MP-133'] = 'values'

        elif self.world_name == WorldNames.Laboratory:
            base_items['Glok-17'] = 'values'
            base_items['9.19mm Bullet Case'] = 'values'

        return base_items







