"""001_initial_users — Create users table for Auth Service.

Mirrors the monolith's CustomUser model schema exactly.

Revision ID: 001
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(254), nullable=False, unique=True),
        sa.Column("username", sa.String(30), nullable=False, unique=True),
        sa.Column("full_name", sa.String(100), server_default=""),
        sa.Column("avatar", sa.String(200), server_default=""),
        sa.Column("native_language", sa.String(10), server_default="uz"),
        sa.Column("learning_language", sa.String(10), server_default="en"),
        sa.Column("proficiency_level", sa.String(2), server_default="A1"),
        sa.Column("daily_goal", sa.Integer(), server_default="10"),
        sa.Column("timezone", sa.String(50), server_default="Asia/Tashkent"),
        sa.Column("is_premium", sa.Boolean(), server_default="false"),
        sa.Column("premium_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("is_staff", sa.Boolean(), server_default="false"),
        sa.Column("is_superuser", sa.Boolean(), server_default="false"),
        sa.Column("has_completed_onboarding", sa.Boolean(), server_default="false"),
        sa.Column("password", sa.String(128), nullable=False),
        sa.Column("date_joined", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_username", "users", ["username"])


def downgrade() -> None:
    op.drop_index("ix_users_username")
    op.drop_index("ix_users_email")
    op.drop_table("users")
