"""add fetched_at in Rss

Revision ID: 333e9d968469
Revises: 4e5868d06707
Create Date: 2024-10-02 17:04:26.406196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '333e9d968469'
down_revision: Union[str, None] = '4e5868d06707'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rss', sa.Column('fetched_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rss', 'fetched_at')
    # ### end Alembic commands ###