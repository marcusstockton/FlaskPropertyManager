"""Added property images table

Revision ID: f7212d4ee1e0
Revises: a9f85dc67a8e
Create Date: 2022-04-27 08:50:15.577736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7212d4ee1e0'
down_revision = 'a9f85dc67a8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('propertyImages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], name=op.f('fk_propertyImages_property_id_property')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_propertyImages'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('propertyImages')
    # ### end Alembic commands ###
