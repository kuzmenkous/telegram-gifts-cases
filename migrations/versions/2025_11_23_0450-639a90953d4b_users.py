# mypy: ignore-errors
# ruff: noqa: INP001
"""users.

Revision ID: 639a90953d4b
Revises: 1cd355259908
Create Date: 2025-11-23 04:50:29.387481

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from alembic_utils.pg_trigger import PGTrigger

# revision identifiers, used by Alembic.
revision: str = "639a90953d4b"
down_revision: str | None = "1cd355259908"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id", sa.BigInteger(), sa.Identity(always=False), nullable=False
        ),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("stars", sa.Integer(), server_default="0", nullable=False),
        sa.Column("tickets", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
    )
    op.create_index(
        op.f("ix__users__telegram_id"), "users", ["telegram_id"], unique=True
    )
    op.create_index(
        op.f("ix__users__username"), "users", ["username"], unique=True
    )

    core_users_update_users_updated_at = PGTrigger(
        schema="core",
        signature="update_users_updated_at",
        on_entity="core.users",
        is_constraint=False,
        definition="BEFORE UPDATE ON users\nFOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
    )
    op.create_entity(core_users_update_users_updated_at)


def downgrade() -> None:
    op.drop_index(op.f("ix__users__username"), table_name="users")
    op.drop_index(op.f("ix__users__telegram_id"), table_name="users")

    core_users_update_users_updated_at = PGTrigger(
        schema="core",
        signature="update_users_updated_at",
        on_entity="core.users",
        is_constraint=False,
        definition="BEFORE UPDATE ON users\nFOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
    )
    op.drop_entity(core_users_update_users_updated_at)

    op.drop_table("users")
