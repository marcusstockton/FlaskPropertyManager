"""'Adding_Contact_details_to_tenant_model'

Revision ID: e565d498bcbd
Revises: b08ed380617c
Create Date: 2020-10-25 22:12:59.324396

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e565d498bcbd'
down_revision = 'b08ed380617c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_address', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.drop_column('phone_number')
        batch_op.drop_column('email_address')

    # ### end Alembic commands ###