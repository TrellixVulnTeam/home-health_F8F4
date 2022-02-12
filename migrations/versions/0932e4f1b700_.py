"""empty message

Revision ID: 0932e4f1b700
Revises: ddac0ac85693
Create Date: 2022-02-12 02:18:41.080295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0932e4f1b700'
down_revision = 'ddac0ac85693'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('packet', 'packet_count_store')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packet', sa.Column('packet_count_store', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###