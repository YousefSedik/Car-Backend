"""remove car_speed col for User Model.

Revision ID: bdd8b0806712
Revises: fe9a9b9166a9
Create Date: 2024-12-24 23:51:11.708486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bdd8b0806712'
down_revision: Union[str, None] = 'fe9a9b9166a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'car_speed')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('car_speed', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
