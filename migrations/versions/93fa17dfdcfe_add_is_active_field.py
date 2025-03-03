"""Add is_active field

Revision ID: 93fa17dfdcfe
Revises: 1d3bb02774e2
Create Date: 2024-12-02 15:22:47.463203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93fa17dfdcfe'
down_revision = '1d3bb02774e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
