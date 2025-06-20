"""Initial baseline

Revision ID: b0b7765d8722
Revises: 
Create Date: 2025-06-05 00:39:44.726310

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b0b7765d8722'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reward_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('quantity_available', sa.Integer(), nullable=False),
    sa.Column('price_tokens', sa.Float(), nullable=False),
    sa.Column('unit_price_fcfa', sa.Float(), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reward_id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['accounts_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('lot_notifications')
    op.drop_table('lot_stock')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lot_stock',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('reward_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('quantity_available', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('last_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['reward_id'], ['lot_recompenses.id'], name='lot_stock_reward_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='lot_stock_pkey')
    )
    op.create_table('lot_notifications',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['accounts_account.id'], name='lot_notifications_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='lot_notifications_pkey')
    )
    op.drop_table('notifications')
    op.drop_table('stock')
    # ### end Alembic commands ###
