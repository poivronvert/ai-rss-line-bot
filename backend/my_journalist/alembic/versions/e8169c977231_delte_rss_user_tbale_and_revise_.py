"""delte rss_user tbale and revise collections user_id type

Revision ID: e8169c977231
Revises: f8549126643f
Create Date: 2024-11-12 13:56:58.505986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8169c977231'
down_revision: Union[str, None] = 'f8549126643f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rss_users')
    op.alter_column('collections', 'user_id',
               existing_type=sa.UUID(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('collections', 'user_id',
               existing_type=sa.String(),
               type_=sa.UUID(),
               existing_nullable=False)
    op.create_table('rss_users',
    sa.Column('rss_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['rss_id'], ['rss.id'], name='rss_users_rss_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='rss_users_user_id_fkey'),
    sa.PrimaryKeyConstraint('rss_id', 'user_id', name='rss_users_pkey')
    )
    # ### end Alembic commands ###