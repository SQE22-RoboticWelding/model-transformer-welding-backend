"""template_language_extension

Revision ID: 7a6781dac3d6
Revises: 1140f5f756c0
Create Date: 2022-07-04 03:28:44.627130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a6781dac3d6'
down_revision = '1140f5f756c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("TRUNCATE robottype, robot, weldingpoint, generationtemplate;")
    op.add_column('generationtemplate', sa.Column('language', sa.String(), nullable=True))
    op.add_column('generationtemplate', sa.Column('file_extension', sa.String(), nullable=True))
    op.add_column('generationtemplate', sa.Column('version', sa.FLOAT(precision=2), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('generationtemplate', 'file_extension')
    op.drop_column('generationtemplate', 'language')
    op.drop_column('generationtemplate', 'version')
    # ### end Alembic commands ###
