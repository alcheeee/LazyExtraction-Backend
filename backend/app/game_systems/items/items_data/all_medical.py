from .. import (
    ItemType,
    ItemTier,
    MedicalBase,
    Medical,
    StaticItem
)


class Gauze(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Gauze"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 60
    health_adj: int = 6


class CompressionBandage(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Compression Bandage"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 100
    health_adj: int = 8


class Tylopain(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Tylopain"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 80
    pain_reduction: int = 6
    amount_of_actions: int = 3


class Morphine(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Morphine"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 120
    pain_reduction: int = 10
    amount_of_actions: int = 1


class Adrenaline(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Adrenaline"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 200
    agility_adj: int = 10
    strength_adj: int = 5
    amount_of_actions: int = 1


class Ephedrine(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Ephedrine"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 150
    agility_adj: int = 5
    strength_adj: int = 3
    amount_of_actions: int = 2


class FirstAidKit(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "First Aid Kit"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 300
    health_adj: int = 20
    pain_reduction: int = 5
    amount_of_actions: int = 1


class AdvancedFirstAidKit(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Advanced First Aid Kit"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 500
    health_adj: int = 30
    pain_reduction: int = 10
    amount_of_actions: int = 1


class SteroidInjection(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Steroid Injection"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 400
    strength_adj: int = 10
    agility_adj: int = 5
    amount_of_actions: int = 1


class PainReliefInjection(StaticItem, MedicalBase):
    __type__ = Medical
    item_name: str = "Pain Relief Injection"
    category: ItemType = ItemType.Medical
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 250
    pain_reduction: int = 15
    amount_of_actions: int = 1



medical_classes = [
    Gauze,
    CompressionBandage,
    Tylopain,
    Morphine,
    Adrenaline,
    Ephedrine,
    FirstAidKit,
    AdvancedFirstAidKit,
    SteroidInjection,
    PainReliefInjection
]
