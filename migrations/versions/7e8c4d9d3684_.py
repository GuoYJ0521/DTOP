"""empty message

Revision ID: 7e8c4d9d3684
Revises: 1a31dd6e0dfe
Create Date: 2024-08-12 16:17:43.386880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7e8c4d9d3684'
down_revision = '1a31dd6e0dfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('machines', schema=None) as batch_op:
        batch_op.alter_column('machine_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.create_foreign_key(None, 'machine_list', ['machine_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('machines', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('machine_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###
