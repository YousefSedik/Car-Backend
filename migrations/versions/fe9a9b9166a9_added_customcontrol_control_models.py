"""Added CustomControl, Control Models.

Revision ID: fe9a9b9166a9
Revises: dc0693c2f723
Create Date: 2024-12-24 23:48:00.529209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'fe9a9b9166a9'
down_revision: Union[str, None] = 'dc0693c2f723'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customcontrol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('control',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('custom_control_id', sa.Integer(), nullable=False),
    sa.Column('basic_control_id', sa.Integer(), nullable=False),
    sa.Column('distance', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['basic_control_id'], ['basiccontrol.id'], ),
    sa.ForeignKeyConstraint(['custom_control_id'], ['customcontrol.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # op.alter_column('user', 'car_speed',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('user', 'car_speed',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    op.drop_table('control')
    op.drop_table('customcontrol')
    # ### end Alembic commands ###