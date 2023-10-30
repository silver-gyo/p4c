"""empty message

Revision ID: 73473973a7cc
Revises: d0b097a2bf56
Create Date: 2023-10-29 08:13:16.381397

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '73473973a7cc'
down_revision = 'd0b097a2bf56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'users', ['user_idx'], ['idx'], ondelete='CASCADE')
        batch_op.drop_column('user_id')
        batch_op.drop_column('member_name')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_idx', sa.Integer(), server_default='null', nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_idx'], ['idx'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_idx')

    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.add_column(sa.Column('member_name', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
