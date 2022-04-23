"""add last Columns to posts

Revision ID: d67b3581a7a2
Revises: d29c5af1b0a1
Create Date: 2022-04-22 13:00:21.664436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd67b3581a7a2'
down_revision = 'd29c5af1b0a1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                    sa.Column('published',sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column('posts',
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
                )
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
