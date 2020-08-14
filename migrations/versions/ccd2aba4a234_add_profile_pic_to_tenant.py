"""Add Profile Pic to tenant

Revision ID: ccd2aba4a234
Revises: 019ded45b389
Create Date: 2020-07-23 09:53:56.721163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccd2aba4a234'
down_revision = '019ded45b389'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###