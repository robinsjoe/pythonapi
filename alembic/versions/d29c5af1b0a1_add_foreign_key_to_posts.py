"""add foreign key to posts

Revision ID: d29c5af1b0a1
Revises: 4a327a1e3493
Create Date: 2022-04-22 12:48:23.251896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd29c5af1b0a1'
down_revision = '4a327a1e3493'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fkey','posts','users',['user_id'],['id'],None,"CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fkey','posts')
    op.drop_column('posts','user_id')
    pass
