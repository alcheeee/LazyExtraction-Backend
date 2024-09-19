from ...schemas import (
    ItemTier,
    ItemType,
    AttachmentTypes,
    ArmorType,
    ClothingType,

    ItemBase,
    WeaponBase,
    ArmorBase,
    MedicalBase,
    ClothingBase,
    BulletBase,
    AttachmentBase
)

from ...models import (
    Items,
    Armor,
    Weapon,
    Medical,
    Bullets,
    Attachments,
    Clothing
)


class StaticItem(ItemBase):
    def to_db_models(self):
        item_data = self.dict(exclude={'__type__'})
        item = Items(**item_data)
        detail_data = self.dict(exclude={field for field in ItemBase.model_fields})
        detail_class = self.__class__.__type__
        detail = detail_class(**detail_data)
        return item, detail
