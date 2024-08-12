"""add sensor foreign key

Revision ID: f6854dd66e85
Revises: 60fbd7866fb3
Create Date: 2024-08-12 22:45:55.161311

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f6854dd66e85'
down_revision = '60fbd7866fb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensors', schema=None) as batch_op:
        batch_op.alter_column('machine',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.create_foreign_key(None, 'machines', ['machine'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensors', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('machine',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###
