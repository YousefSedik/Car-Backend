"""making distance field to be nullable.

Revision ID: 2399f6709889
Revises: 8e3cc88e619c
Create Date: 2024-12-25 13:57:14.306945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '2399f6709889'
down_revision: Union[str, None] = '8e3cc88e619c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
