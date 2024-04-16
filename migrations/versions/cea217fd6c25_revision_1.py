"""Revision 1

Revision ID: cea217fd6c25
Revises: 904b24fe0033
Create Date: 2024-04-12 15:22:16.692219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'cea217fd6c25'
down_revision: Union[str, None] = '904b24fe0033'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'quality',
               existing_type=mysql.ENUM('Junk', 'Common', 'Uncommon', 'Rare', 'Special', 'Unique'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'quality',
               existing_type=mysql.ENUM('Junk', 'Common', 'Uncommon', 'Rare', 'Special', 'Unique'),
               nullable=False)
    # ### end Alembic commands ###