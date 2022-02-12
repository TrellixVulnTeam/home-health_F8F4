"""packet table

Revision ID: 7dac9b8b53e2
Revises: 1db98b065a16
Create Date: 2022-02-12 01:54:50.121725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dac9b8b53e2'
down_revision = '1db98b065a16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_packet_packet_count_store', table_name='packet')
    op.drop_column('packet', 'packet_count_store')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packet', sa.Column('packet_count_store', sa.INTEGER(), nullable=True))
    op.create_index('ix_packet_packet_count_store', 'packet', ['packet_count_store'], unique=False)
    # ### end Alembic commands ###