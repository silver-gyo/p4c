"""empty message

Revision ID: cb3ac25c545d
Revises: 47648420c457
Create Date: 2023-10-29 08:03:34.068386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb3ac25c545d'
down_revision = '47648420c457'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'users', ['user_idx'], ['idx'], ondelete='CASCADE')
        batch_op.drop_column('user_id')
        batch_op.drop_column('member_name')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_idx', sa.Integer(), nullable=True))
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
