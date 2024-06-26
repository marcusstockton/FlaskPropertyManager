"""Updating relationships to appease pylint

Revision ID: 6645e5442d50
Revises: 3ef4bab79677
Create Date: 2024-05-10 23:30:22.270435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6645e5442d50'
down_revision = '3ef4bab79677'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=4),
               type_=sa.Enum('MR', 'MRS', 'MISS', 'MS', 'LORD', 'SIR', 'DR', 'LADY', 'DAME', 'PROFESSOR', 'MX', name='titleenum'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.Enum('MR', 'MRS', 'MISS', 'MS', 'LORD', 'SIR', 'DR', 'LADY', 'DAME', 'PROFESSOR', 'MX', name='titleenum'),
               type_=sa.VARCHAR(length=4),
               existing_nullable=True)

    # ### end Alembic commands ###
