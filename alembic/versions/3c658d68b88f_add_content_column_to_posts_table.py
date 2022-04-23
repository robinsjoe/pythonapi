"""add Content Column to Posts Table

Revision ID: 3c658d68b88f
Revises: 1a1007a7d061
Create Date: 2022-04-22 12:28:31.661510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c658d68b88f'
down_revision = '1a1007a7d061'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
