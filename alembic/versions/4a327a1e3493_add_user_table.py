"""add User Table

Revision ID: 4a327a1e3493
Revises: 3c658d68b88f
Create Date: 2022-04-22 12:36:00.708470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a327a1e3493'
down_revision = '3c658d68b88f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('name',sa.String(), nullable=False),
                    sa.Column('email',sa.String(), nullable=False, unique=True),
                    sa.Column('password',sa.String(), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
