"""add_workpiece

Revision ID: beedead632c9
Revises: 0decc0e420e7
Create Date: 2022-07-23 22:07:54.566517

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'beedead632c9'
down_revision = '0decc0e420e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("TRUNCATE weldingpoint, robot, project;")
    op.create_table('workpiece',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('project_id', sa.Integer(), nullable=True),
                    sa.Column('model_file_name', sa.String(), nullable=True),
                    sa.Column('model_file', sa.String(), nullable=True),
                    sa.Column('position_x', sa.Float(), nullable=True),
                    sa.Column('position_y', sa.Float(), nullable=True),
                    sa.Column('position_z', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_workpiece_id'), 'workpiece', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workpiece_id'), table_name='workpiece')
    op.drop_table('workpiece')
    # ### end Alembic commands ###