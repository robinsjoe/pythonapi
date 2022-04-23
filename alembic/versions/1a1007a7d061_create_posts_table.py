"""create posts table

Revision ID: 1a1007a7d061
Revises: 
Create Date: 2022-04-22 07:50:46.542596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a1007a7d061'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
