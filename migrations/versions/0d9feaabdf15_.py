"""empty message

Revision ID: 0d9feaabdf15
Revises: 35b1274ad3dc
Create Date: 2023-10-29 02:05:10.549062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d9feaabdf15'
down_revision = '35b1274ad3dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('idx', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=12), nullable=False),
    sa.Column('password_chk', sa.String(length=12), nullable=False),
    sa.Column('name', sa.String(length=5), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('member_name', sa.String(length=10), nullable=False),
    sa.Column('super', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('member_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###