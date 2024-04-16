"""Revision

Revision ID: b9c59f2fc6bf
Revises: b32a8bc5d039
Create Date: 2024-04-16 10:29:29.694440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b9c59f2fc6bf'
down_revision: Union[str, None] = 'b32a8bc5d039'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blackmarket', sa.Column('item_quality', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('generalmarket', sa.Column('item_quality', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_column('items', 'buy_price')
    op.drop_column('weapon', 'damage_bonus')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weapon', sa.Column('damage_bonus', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('items', sa.Column('buy_price', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('generalmarket', 'item_quality')
    op.drop_column('blackmarket', 'item_quality')
    # ### end Alembic commands ###
