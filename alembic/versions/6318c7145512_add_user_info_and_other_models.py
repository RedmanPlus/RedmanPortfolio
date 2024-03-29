"""add user_info and other models

Revision ID: 6318c7145512
Revises: 
Create Date: 2023-03-15 21:19:37.260918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6318c7145512'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skill',
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.Column('skill_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('skill_id'),
    sa.UniqueConstraint('skill_name', name='uix_2')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('email_token',
    sa.Column('token_id', sa.Integer(), nullable=False),
    sa.Column('bearer', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['bearer'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('token_id'),
    sa.UniqueConstraint('key', name='uix_1')
    )
    op.create_table('session',
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('session_key', sa.String(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('session_id'),
    sa.UniqueConstraint('session_key')
    )
    op.create_table('user_info',
    sa.Column('info_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('photo_link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('info_id')
    )
    op.create_table('link',
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.Column('resource', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.info_id'], ),
    sa.PrimaryKeyConstraint('link_id')
    )
    op.create_table('project',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('project_name', sa.String(), nullable=True),
    sa.Column('short_description', sa.String(), nullable=True),
    sa.Column('project_logo', sa.String(), nullable=True),
    sa.Column('full_description', sa.String(), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user_info.info_id'], ),
    sa.PrimaryKeyConstraint('project_id')
    )
    op.create_table('skill_user_m2m',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.Column('skill_lvl', sa.String(length=12), nullable=True),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.skill_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.info_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_block',
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('block_name', sa.String(), nullable=True),
    sa.Column('block_description', sa.String(), nullable=True),
    sa.Column('block_author_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['block_author_id'], ['user_info.info_id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], ),
    sa.PrimaryKeyConstraint('block_id')
    )
    op.create_table('block_block_m2m',
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_id'], ['project_block.block_id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['project_block.block_id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id')
    )
    op.create_table('skill_block_m2m',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['project_block.block_id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.skill_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skill_block_m2m')
    op.drop_table('block_block_m2m')
    op.drop_table('project_block')
    op.drop_table('skill_user_m2m')
    op.drop_table('project')
    op.drop_table('link')
    op.drop_table('user_info')
    op.drop_table('session')
    op.drop_table('email_token')
    op.drop_table('user')
    op.drop_table('skill')
    # ### end Alembic commands ###
