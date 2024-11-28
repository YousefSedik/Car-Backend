"""Create User Table

Revision ID: d7d6c368cf75
Revises: ac1a4046d93b
Create Date: 2024-11-27 20:52:43.504534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd7d6c368cf75'
down_revision: Union[str, None] = 'ac1a4046d93b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
