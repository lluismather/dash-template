"""create_oauth_table

Revision ID: 20240707115637
Revises: 20240707115213
Create Date: 2024-07-07 11:56:37.587149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20240707115637'
down_revision = '20240707115213'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "flask_dance_oauth",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("provider_user_id", sa.String(256), unique=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("provider", sa.String(256)),
        sa.Column("token", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table("oauth")
