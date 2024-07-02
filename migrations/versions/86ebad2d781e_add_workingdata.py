"""add WorkingData

Revision ID: 86ebad2d781e
Revises: 9bc99c8680f3
Create Date: 2024-07-02 20:11:20.105979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86ebad2d781e'
down_revision = '9bc99c8680f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('working_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('machine_id', sa.Integer(), nullable=True),
    sa.Column('x', sa.Float(), nullable=True),
    sa.Column('y', sa.Float(), nullable=True),
    sa.Column('z', sa.Float(), nullable=True),
    sa.Column('speed', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('working_data')
    # ### end Alembic commands ###
