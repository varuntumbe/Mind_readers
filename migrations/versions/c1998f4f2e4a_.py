"""empty message

Revision ID: c1998f4f2e4a
Revises: 19cd13b57a39
Create Date: 2020-09-28 10:32:37.278265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1998f4f2e4a'
down_revision = '19cd13b57a39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile') as batch_op:
        batch_op.add_column('profile', sa.Column('first_name', sa.String(length=25), nullable=True))
    # with op.batch_alter_table('profile') as batch_op:
    #     batch_op.add_column('profile', sa.Column('last_name', sa.String(length=25), nullable=True))
    # with op.batch_alter_table('profile') as batch_op:
    #     batch_op.add_column('profile', sa.Column('qualification', sa.String(length=50), nullable=True))
    # with op.batch_alter_table('profile') as batch_op:
    #     batch_op.drop_column('profile', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('psycologists', 'email',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.add_column('profile', sa.Column('name', sa.VARCHAR(length=25), nullable=True))
    op.drop_column('profile', 'qualification')
    op.drop_column('profile', 'last_name')
    op.drop_column('profile', 'first_name')
    # ### end Alembic commands ###
