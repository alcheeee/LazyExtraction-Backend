"""
Stat types:
Health
Intelligence
Knowledge
Strength
Stamina (maybe Energy?)
"""

default_user_stats = {
    #Example id = 1
    'Level': 1,
    'Health': 100,
    'Intelligence': 1,
    'Knowledge': 1,
    'Strength': 1,
    'Stamina': 100
}

class UserStats():
    def __init__(self, id: int, user_stats: dict):
        self.id = id
        self.level = user_stats['Level']
        self.health = user_stats['Health']
        self.intelligence = user_stats['Intelligence']
        self.knowledge = user_stats['Knowledge']
        self.strength = user_stats['Strength']
        self.stamina = user_stats['Stamina']


UserStats(1, default_user_stats)

