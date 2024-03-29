"""empty message

Revision ID: 47648420c457
Revises: e15295fb61a9
Create Date: 2023-10-29 08:00:22.576566

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '47648420c457'
down_revision = 'e15295fb61a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_idx', sa.Integer(), server_default='1', nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_idx'], ['idx'], ondelete='CASCADE')
        batch_op.drop_column('member_name')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_idx', sa.Integer(), server_default='1', nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_idx'], ['idx'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_idx')

    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('member_name', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_idx')

    # ### end Alembic commands ###
