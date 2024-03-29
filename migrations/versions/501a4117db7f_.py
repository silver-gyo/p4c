"""empty message

Revision ID: 501a4117db7f
Revises: 0d9feaabdf15
Create Date: 2023-10-29 02:12:58.473886

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '501a4117db7f'
down_revision = '0d9feaabdf15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=12),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('password_chk',
               existing_type=mysql.VARCHAR(length=12),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_chk',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=12),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=12),
               existing_nullable=False)

    # ### end Alembic commands ###
