"""empty message

Revision ID: eb9cb64cfdee
Revises: a1f47f78f171
Create Date: 2023-10-28 18:01:31.382056

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eb9cb64cfdee'
down_revision = 'a1f47f78f171'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.drop_column('secret_YN')
        batch_op.drop_column('file_YN')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_YN', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('secret_YN', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
