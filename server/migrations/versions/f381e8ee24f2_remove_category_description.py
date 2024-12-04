"""remove category description

Revision ID: f381e8ee24f2
Revises: e375813ec118
Create Date: 2024-12-04 00:10:50.290314

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Column


# revision identifiers, used by Alembic.
revision = 'f381e8ee24f2'
down_revision = 'e375813ec118'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("category") as batch_op:
        batch_op.drop_column("description")


def downgrade():
    with op.batch_alter_table("category") as batch_op:
        batch_op.add_column(Column("description", sa.String(length=200), nullable=True))
