"""empty message

Revision ID: dc80b00aa242
Revises: 8d31109c41cb
Create Date: 2020-09-18 13:07:13.461689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc80b00aa242'
down_revision = '8d31109c41cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('psycologists', 'email',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('psycologists', 'email',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###
