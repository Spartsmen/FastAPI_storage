"""referals creation

Revision ID: 9287210d93f2
Revises: 24423b1eae53
Create Date: 2023-10-30 15:45:54.420657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9287210d93f2'
down_revision: Union[str, None] = '24423b1eae53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('referals',
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['target_id'], ['document.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('referals')
    # ### end Alembic commands ###
