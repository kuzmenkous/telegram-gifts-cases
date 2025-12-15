# mypy: ignore-errors
# ruff: noqa: INP001
"""create_non_table_schema_items.

Revision ID: feb115297fc8
Revises: 9d48f7f1561c
Create Date: 2025-11-15 08:11:18.130829

"""

from collections.abc import Sequence

from alembic import op
from alembic_utils.pg_function import PGFunction

# revision identifiers, used by Alembic.
revision: str = "feb115297fc8"
down_revision: str | None = "9d48f7f1561c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    core_update_updated_at_column = PGFunction(
        schema="core",
        signature="update_updated_at_column()",
        definition="RETURNS TRIGGER AS $$\nBEGIN\n    NEW.updated_at = NOW();\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql",
    )
    op.create_entity(core_update_updated_at_column)


def downgrade() -> None:
    core_update_updated_at_column = PGFunction(
        schema="core",
        signature="update_updated_at_column()",
        definition="RETURNS TRIGGER AS $$\nBEGIN\n    NEW.updated_at = NOW();\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql",
    )
    op.drop_entity(core_update_updated_at_column)
