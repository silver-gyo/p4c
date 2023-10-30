"""empty message

Revision ID: 5721ed7a525e
Revises: c436f7464c27
Create Date: 2023-10-28 22:19:30.979907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5721ed7a525e'
down_revision = 'c436f7464c27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notice',
    sa.Column('idx', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.Column('content', sa.String(length=200), nullable=False),
    sa.Column('write_t', sa.DateTime(), nullable=False),
    sa.Column('filename', sa.String(length=100), nullable=True),
    sa.Column('file_path', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('idx')
    )
    op.create_table('notice_comment',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('board_idx', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=100), nullable=False),
    sa.Column('write_t', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['board_idx'], ['board.idx'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idx')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notice_comment')
    op.drop_table('notice')
    # ### end Alembic commands ###