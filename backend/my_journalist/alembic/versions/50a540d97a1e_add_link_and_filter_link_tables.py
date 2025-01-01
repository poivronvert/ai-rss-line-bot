"""add link and filter link tables

Revision ID: 50a540d97a1e
Revises: 4b9563c7ff13
Create Date: 2024-10-01 22:55:33.070202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50a540d97a1e'
down_revision: Union[str, None] = '4b9563c7ff13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filtered_links',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('links',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('published_at', sa.DateTime(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_links_link'), 'links', ['link'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_links_link'), table_name='links')
    op.drop_table('links')
    op.drop_table('filtered_links')
    # ### end Alembic commands ###
