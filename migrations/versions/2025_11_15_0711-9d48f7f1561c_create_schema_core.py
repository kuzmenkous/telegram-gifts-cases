# mypy: ignore-errors
# ruff: noqa: INP001
"""create_schema_core.

Revision ID: 9d48f7f1561c
Revises:
Create Date: 2025-11-15 07:11:46.823112

"""

from collections.abc import Sequence

from alembic import op

from src.core.config import settings

# revision identifiers, used by Alembic.
revision: str = "9d48f7f1561c"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {settings.db.schema_name}")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(f"DROP SCHEMA IF EXISTS {settings.db.schema_name} CASCADE")
