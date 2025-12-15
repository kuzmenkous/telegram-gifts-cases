from migrations.queries.ddl import updated_at

entities = (entity for module in (updated_at,) for entity in module.entities)
