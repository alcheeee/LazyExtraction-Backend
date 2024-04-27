"""Init

Revision ID: e204896eab21
Revises: 
Create Date: 2024-04-25 14:09:08.877085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e204896eab21'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('industrialcraftingrecipes')
    op.alter_column('items', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_table('industrialcraftingrecipes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('item_one', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('item_one_amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('item_two', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('item_two_amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('item_three', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('item_three_amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('produced_item_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['produced_item_id'], ['items.id'], name='industrialcraftingrecipes_produced_item_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='industrialcraftingrecipes_pkey')
    )
    # ### end Alembic commands ###