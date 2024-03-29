"""empty message

Revision ID: 296bd4cae995
Revises: c8f8bf9d94c0
Create Date: 2023-10-29 04:15:54.782008

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '296bd4cae995'
down_revision = 'c8f8bf9d94c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.alter_column('member_name',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.String(length=10),
               existing_nullable=False)
        batch_op.create_foreign_key(None, 'users', ['member_name'], ['member_name'])

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('member_name', sa.String(length=10), nullable=False))
        batch_op.create_foreign_key(None, 'users', ['member_name'], ['member_name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('member_name')

    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('member_name',
               existing_type=sa.String(length=10),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=False)

    # ### end Alembic commands ###
