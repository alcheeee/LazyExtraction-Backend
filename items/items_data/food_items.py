
food_attributes_examples = {
    'rarities': ['Junk', 'Common', 'Uncommon',
                 'Rare', 'Special', 'Unique'
            ],
    'health_affect': None,  # 1
    'stamina_affect': None, # 2
    'strength_affect': None, # 3
}

class FoodItem():
    def __init__(self, id: int, rarity: str, affects: list):
        self.id = id
        self.affects = affects
        self.rarity = rarity


food_items = {
    # 'FOOD NAME': FoodItem(id, rarity, [HEALTH, STAMINA, STRENGTH])
    'Apple': FoodItem(1000, 'Junk', [5, 3, 0])
}
