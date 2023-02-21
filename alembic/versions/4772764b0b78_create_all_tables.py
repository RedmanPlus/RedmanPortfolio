"""create all tables

Revision ID: 4772764b0b78
Revises: 
Create Date: 2023-02-22 00:49:01.386418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4772764b0b78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('session',
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('session_key', sa.String(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('session_id'),
    sa.UniqueConstraint('session_key')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session')
    op.drop_table('user')
    # ### end Alembic commands ###