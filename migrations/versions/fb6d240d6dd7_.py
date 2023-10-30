"""empty message

Revision ID: fb6d240d6dd7
Revises: 72080b49bef1
Create Date: 2023-10-30 01:29:50.793358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb6d240d6dd7'
down_revision = '72080b49bef1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notice_like',
    sa.Column('user_idx', sa.Integer(), nullable=False),
    sa.Column('board_idx', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['board_idx'], ['board.idx'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_idx'], ['users.idx'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_idx', 'board_idx')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notice_like')
    # ### end Alembic commands ###