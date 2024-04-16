"""Revision

Revision ID: b32a8bc5d039
Revises: 030b7865897c
Create Date: 2024-04-16 09:31:46.804400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b32a8bc5d039'
down_revision: Union[str, None] = '030b7865897c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'hash',
               existing_type=mysql.INTEGER(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'hash',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
