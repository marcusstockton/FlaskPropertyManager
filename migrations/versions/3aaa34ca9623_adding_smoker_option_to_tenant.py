"""Adding Smoker option to tenant

Revision ID: 3aaa34ca9623
Revises: fb78f1b780b7
Create Date: 2023-11-17 18:37:36.136073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3aaa34ca9623"
down_revision = "fb78f1b780b7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tenant", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "smoker",
                sa.Boolean(),
                nullable=False,
                default=False,
                server_default="False",
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("tenant", schema=None) as batch_op:
        batch_op.drop_column("smoker")

    # ### end Alembic commands ###
