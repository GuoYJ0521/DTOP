"""empty message

Revision ID: 7201e9181da9
Revises: 7e8c4d9d3684
Create Date: 2024-08-12 17:15:42.475188

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7201e9181da9'
down_revision = '7e8c4d9d3684'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensors', schema=None) as batch_op:
        batch_op.alter_column('sensor_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensors', schema=None) as batch_op:
        batch_op.alter_column('sensor_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###
