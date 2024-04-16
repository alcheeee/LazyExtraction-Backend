"""Revision

Revision ID: f6f208915d7a
Revises: 21875eefa05c
Create Date: 2024-04-15 21:19:15.063630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f6f208915d7a'
down_revision: Union[str, None] = '21875eefa05c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'hash',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'hash',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
