"""empty message

Revision ID: e45b0c91fe33
Revises: 
Create Date: 2024-06-07 18:10:30.326629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e45b0c91fe33'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('laptop',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('processor', sa.Integer(), nullable=False),
    sa.Column('ram_memory', sa.Integer(), nullable=False),
    sa.Column('display_size', sa.Float(), nullable=False),
    sa.Column('storage_capacity', sa.Integer(), nullable=False),
    sa.Column('cpu_cores', sa.Integer(), nullable=False),
    sa.Column('graphics_card', sa.Float(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('reviews', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('tracked_product', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('tracked_product'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('laptop')
    # ### end Alembic commands ###
