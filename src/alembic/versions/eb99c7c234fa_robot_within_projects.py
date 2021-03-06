"""robot within projects

Revision ID: eb99c7c234fa
Revises: ad7ddf800853
Create Date: 2022-06-30 14:24:13.593114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb99c7c234fa'
down_revision = 'ad7ddf800853'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("TRUNCATE weldingpoint, robot;")
    op.add_column('robot', sa.Column('project_id', sa.Integer(), nullable=True))
    op.add_column('robot', sa.Column('name', sa.String(), nullable=True))
    op.add_column('robot', sa.Column('position_x', sa.Float(), nullable=True))
    op.add_column('robot', sa.Column('position_y', sa.Float(), nullable=True))
    op.add_column('robot', sa.Column('position_z', sa.Float(), nullable=True))
    op.add_column('robot', sa.Column('position_norm_vector_x', sa.Float(), nullable=True))
    op.add_column('robot', sa.Column('position_norm_vector_y', sa.Float(), nullable=True))
    op.add_column('robot', sa.Column('position_norm_vector_z', sa.Float(), nullable=True))
    op.create_foreign_key(None, 'robot', 'project', ['project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'robot', type_='foreignkey')
    op.drop_column('robot', 'position_norm_vector_z')
    op.drop_column('robot', 'position_norm_vector_y')
    op.drop_column('robot', 'position_norm_vector_x')
    op.drop_column('robot', 'position_z')
    op.drop_column('robot', 'position_y')
    op.drop_column('robot', 'position_x')
    op.drop_column('robot', 'name')
    op.drop_column('robot', 'project_id')
    # ### end Alembic commands ###
