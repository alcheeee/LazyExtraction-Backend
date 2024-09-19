from typing import Optional, List, Any, Sequence
from sqlalchemy import select, update, values, delete, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from .stats_crud import StatsCRUD
from ..models import (
    User,
    Inventory,
    InventoryItem,
    Stats,
    Items,
    Weapon,
    Bullets,
    Attachments
)
