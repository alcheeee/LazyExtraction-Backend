"""Revision friends

Revision ID: 59270dbf5d1d
Revises: 844479fdd25d
Create Date: 2024-04-22 10:59:25.783489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '59270dbf5d1d'
down_revision: Union[str, None] = '844479fdd25d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('friendassociation')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friendassociation',
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('friend_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['user.id'], name='friendassociation_ibfk_2'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='friendassociation_ibfk_1'),
    sa.PrimaryKeyConstraint('user_id', 'friend_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
