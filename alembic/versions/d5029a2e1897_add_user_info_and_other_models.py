"""add user_info and other models

Revision ID: d5029a2e1897
Revises: b0dab5b8c64a
Create Date: 2023-03-17 22:50:37.954635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5029a2e1897'
down_revision = 'b0dab5b8c64a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workplace',
    sa.Column('workplace_id', sa.Integer(), nullable=False),
    sa.Column('workplace_name', sa.String(), nullable=True),
    sa.Column('work_start_date', sa.Date(), nullable=True),
    sa.Column('work_end_date', sa.Date(), nullable=True),
    sa.Column('is_current_workplace', sa.Boolean(), nullable=True),
    sa.Column('company_link', sa.String(), nullable=True),
    sa.Column('workplace_decsription', sa.String(), nullable=True),
    sa.Column('worker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['worker_id'], ['user_info.info_id'], ),
    sa.PrimaryKeyConstraint('workplace_id')
    )
    op.create_table('skill_workplace_m2m',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workplace_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.skill_id'], ),
    sa.ForeignKeyConstraint(['workplace_id'], ['workplace.workplace_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('project', sa.Column('workplace_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'project', 'workplace', ['workplace_id'], ['workplace_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_column('project', 'workplace_id')
    op.drop_table('skill_workplace_m2m')
    op.drop_table('workplace')
    # ### end Alembic commands ###