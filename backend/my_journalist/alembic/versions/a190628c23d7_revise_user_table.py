"""revise user table

Revision ID: a190628c23d7
Revises: 36716e4edd9f
Create Date: 2024-12-06 17:23:18.878120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a190628c23d7'
down_revision: Union[str, None] = '36716e4edd9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'displayName', new_column_name='name')
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))
    op.alter_column('users', 'pictureUrl',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('displayName', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('users', 'pictureUrl',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'password')
    op.drop_column('users', 'name')
    op.create_table('news_vector_table',
    sa.Column('langchain_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=False),
    sa.Column('langchain_metadata', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('langchain_id', name='news_vector_table_pkey')
    )
    # ### end Alembic commands ###
