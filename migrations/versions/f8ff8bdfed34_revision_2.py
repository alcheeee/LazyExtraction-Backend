"""Revision 2

Revision ID: f8ff8bdfed34
Revises: cea217fd6c25
Create Date: 2024-04-12 15:57:03.066666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f8ff8bdfed34'
down_revision: Union[str, None] = 'cea217fd6c25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stats', sa.Column('luck', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stats', 'luck')
    # ### end Alembic commands ###