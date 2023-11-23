"""Db creation 2

Revision ID: 6d79aca749ff
Revises: d3c15f033895
Create Date: 2023-11-15 17:27:48.459253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d79aca749ff'
down_revision: Union[str, None] = 'd3c15f033895'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referrals',
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['target_id'], ['document.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('referrals')
    op.drop_table('document')
    op.drop_table('user')
    # ### end Alembic commands ###