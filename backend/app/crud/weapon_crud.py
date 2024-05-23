from sqlalchemy import select, update
from .base_crud import BaseCRUD
from ..models import (
    User,
    Inventory,
    Stats,
    Items,
    Weapon,
    Bullets,
    Attachments
)


class WeaponCRUD(BaseCRUD):
    pass

