from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

from src.core.config import settings
from src.models.base import metadata

entities = [
    PGFunction(
        schema=settings.db.user,
        signature="update_updated_at_column()",
        definition="""RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql""",
    )
]

entities.extend(
    PGTrigger(  # type: ignore[misc]
        schema=settings.db.user,
        signature=f"update_{table_name}_updated_at",
        definition=f"""BEFORE UPDATE ON {table_name}
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()""",
        on_entity=f"{settings.db.user}.{table_name}",
    )
    for table_name in metadata.tables
)
