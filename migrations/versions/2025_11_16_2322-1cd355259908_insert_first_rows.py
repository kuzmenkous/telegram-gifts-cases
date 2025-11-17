# mypy: ignore-errors
# ruff: noqa: INP001
"""insert first rows.

Revision ID: 1cd355259908
Revises: 751bdc2406af
Create Date: 2025-11-16 23:22:40.574212

"""

from collections.abc import Sequence

from alembic import op

from migrations.queries.first_rows import (
    insert_first_rows_with_async_connection,
)

# revision identifiers, used by Alembic.
revision: str = "1cd355259908"
down_revision: str | None = "751bdc2406af"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.run_async(insert_first_rows_with_async_connection)


def downgrade() -> None:
    """Downgrade schema."""
