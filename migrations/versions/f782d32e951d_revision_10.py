"""Revision 10

Revision ID: f782d32e951d
Revises: c40c6b78c693
Create Date: 2024-04-16 12:22:50.396010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f782d32e951d'
down_revision: Union[str, None] = 'c40c6b78c693'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'inventory', 'items', ['equipped_mask'], ['id'])
    op.create_foreign_key(None, 'inventory', 'items', ['equipped_legs'], ['id'])
    op.create_foreign_key(None, 'inventory', 'items', ['equipped_body'], ['id'])
    op.drop_column('inventory', 'cash')
    op.drop_column('inventory', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('inventory', sa.Column('cash', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'inventory', type_='foreignkey')
    op.drop_constraint(None, 'inventory', type_='foreignkey')
    op.drop_constraint(None, 'inventory', type_='foreignkey')
    # ### end Alembic commands ###