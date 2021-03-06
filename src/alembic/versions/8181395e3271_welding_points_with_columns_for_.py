"""welding points with columns for original coordinates

Revision ID: 8181395e3271
Revises: 7a6781dac3d6
Create Date: 2022-07-07 14:54:36.643993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8181395e3271'
down_revision = '7a6781dac3d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('generationtemplate', 'version',
               existing_type=sa.REAL(),
               type_=sa.FLOAT(precision=2),
               existing_nullable=False)
    op.add_column('weldingpoint', sa.Column('x_original', sa.Float(), nullable=True))
    op.add_column('weldingpoint', sa.Column('y_original', sa.Float(), nullable=True))
    op.add_column('weldingpoint', sa.Column('z_original', sa.Float(), nullable=True))
    op.execute("UPDATE weldingpoint SET x_original = x, y_original = y, z_original = z;")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weldingpoint', 'z_original')
    op.drop_column('weldingpoint', 'y_original')
    op.drop_column('weldingpoint', 'x_original')
    op.alter_column('generationtemplate', 'version',
               existing_type=sa.FLOAT(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
