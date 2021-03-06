"""create relationship WaterSprinkler and Plants

Revision ID: 52e3c41e28b9
Revises: 16720f290532
Create Date: 2022-04-05 13:08:21.719100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52e3c41e28b9'
down_revision = '16720f290532'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plants', sa.Column('water_sprinklers_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'plants', 'water_sprinklers', ['water_sprinklers_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'plants', type_='foreignkey')
    op.drop_column('plants', 'water_sprinklers_id')
    # ### end Alembic commands ###
