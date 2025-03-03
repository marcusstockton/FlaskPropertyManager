"""finished moving tenant model to mapped_column style

Revision ID: 919cedb909f4
Revises: 4e502075deff
Create Date: 2025-02-24 20:55:24.768528

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '919cedb909f4'
down_revision = '4e502075deff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document-type', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.alter_column('purchase_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10),
               existing_nullable=True)
        batch_op.alter_column('monthly_rental_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10),
               existing_nullable=True)

    with op.batch_alter_table('tenant-document', schema=None) as batch_op:
        batch_op.alter_column('tenant_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('document_blob',
               existing_type=postgresql.BYTEA(),
               nullable=False)
        batch_op.alter_column('file_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('file_ext',
               existing_type=sa.VARCHAR(length=4),
               nullable=False)
        batch_op.alter_column('document_type_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('tenant-profile', schema=None) as batch_op:
        batch_op.alter_column('tenant_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('image',
               existing_type=postgresql.BYTEA(),
               nullable=False)

    with op.batch_alter_table('tenantNote', schema=None) as batch_op:
        batch_op.alter_column('tenant_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('note',
               existing_type=sa.VARCHAR(length=2000),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenantNote', schema=None) as batch_op:
        batch_op.alter_column('note',
               existing_type=sa.VARCHAR(length=2000),
               nullable=True)
        batch_op.alter_column('tenant_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('tenant-profile', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=postgresql.BYTEA(),
               nullable=True)
        batch_op.alter_column('tenant_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('tenant-document', schema=None) as batch_op:
        batch_op.alter_column('document_type_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('file_ext',
               existing_type=sa.VARCHAR(length=4),
               nullable=True)
        batch_op.alter_column('file_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('document_blob',
               existing_type=postgresql.BYTEA(),
               nullable=True)
        batch_op.alter_column('tenant_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.alter_column('monthly_rental_price',
               existing_type=sa.Float(precision=10),
               type_=sa.REAL(),
               existing_nullable=True)
        batch_op.alter_column('purchase_price',
               existing_type=sa.Float(precision=10),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('document-type', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###
