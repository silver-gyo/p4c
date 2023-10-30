"""empty message

Revision ID: 1c6cc9df1197
Revises: 5721ed7a525e
Create Date: 2023-10-28 22:20:25.607727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6cc9df1197'
down_revision = '5721ed7a525e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notice_comment', schema=None) as batch_op:
        batch_op.drop_constraint('notice_comment_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'notice', ['board_idx'], ['idx'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notice_comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('notice_comment_ibfk_1', 'board', ['board_idx'], ['idx'], ondelete='CASCADE')

    # ### end Alembic commands ###