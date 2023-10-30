"""empty message

Revision ID: c436f7464c27
Revises: eb9cb64cfdee
Create Date: 2023-10-28 19:31:03.954657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c436f7464c27'
down_revision = 'eb9cb64cfdee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.add_column(sa.Column('filename', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('file_path', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.drop_column('file_path')
        batch_op.drop_column('filename')

    # ### end Alembic commands ###