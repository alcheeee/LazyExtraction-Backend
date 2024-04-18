"""Revision 11

Revision ID: d11199d6b289
Revises: 074e620e9053
Create Date: 2024-04-16 16:00:05.600228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd11199d6b289'
down_revision: Union[str, None] = '074e620e9053'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('inventory_ibfk_4', 'inventory', type_='foreignkey')
    op.drop_constraint('inventory_ibfk_3', 'inventory', type_='foreignkey')
    op.drop_constraint('inventory_ibfk_2', 'inventory', type_='foreignkey')
    op.drop_constraint('inventory_ibfk_1', 'inventory', type_='foreignkey')
    op.drop_column('inventory', 'inventory_items')
    op.drop_column('inventory', 'equipped_body')
    op.drop_column('inventory', 'equipped_legs')
    op.drop_column('inventory', 'equipped_weapon')
    op.drop_column('inventory', 'equipped_mask')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('equipped_mask', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('inventory', sa.Column('equipped_weapon', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('inventory', sa.Column('equipped_legs', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('inventory', sa.Column('equipped_body', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('inventory', sa.Column('inventory_items', mysql.VARCHAR(length=255), nullable=False))
    op.create_foreign_key('inventory_ibfk_1', 'inventory', 'items', ['equipped_weapon'], ['id'])
    op.create_foreign_key('inventory_ibfk_2', 'inventory', 'items', ['equipped_mask'], ['id'])
    op.create_foreign_key('inventory_ibfk_3', 'inventory', 'items', ['equipped_legs'], ['id'])
    op.create_foreign_key('inventory_ibfk_4', 'inventory', 'items', ['equipped_body'], ['id'])
    # ### end Alembic commands ###
