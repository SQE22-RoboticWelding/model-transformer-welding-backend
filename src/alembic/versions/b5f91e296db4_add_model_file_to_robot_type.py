"""add model file to robot type

Revision ID: b5f91e296db4
Revises: 569492230e65
Create Date: 2022-07-14 16:35:03.583857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5f91e296db4'
down_revision = '569492230e65'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('generationtemplate', 'version',
               existing_type=sa.REAL(),
               type_=sa.FLOAT(precision=2),
               existing_nullable=False)
    op.add_column('robottype', sa.Column('model_file', sa.String(), nullable=True))
    op.alter_column('robottype', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('robottype', 'vendor',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('robottype', 'vendor',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('robottype', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('robottype', 'model_file')
    op.alter_column('generationtemplate', 'version',
               existing_type=sa.FLOAT(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
