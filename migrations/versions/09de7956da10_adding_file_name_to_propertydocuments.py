"""Adding file name to propertydocuments

Revision ID: 09de7956da10
Revises: f037987ddcc7
Create Date: 2022-07-19 08:26:11.879049

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '09de7956da10'
down_revision = 'f037987ddcc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propertyImages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_name', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propertyImages', schema=None) as batch_op:
        batch_op.drop_column('file_name')

    # ### end Alembic commands ###