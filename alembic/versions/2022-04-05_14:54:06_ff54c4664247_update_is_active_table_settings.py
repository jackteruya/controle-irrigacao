"""update is_active table settings

Revision ID: ff54c4664247
Revises: 01b54aaf7877
Create Date: 2022-04-05 14:54:06.387030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff54c4664247'
down_revision = '01b54aaf7877'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('settings', sa.Column('is_active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'is_active')
    # ### end Alembic commands ###
