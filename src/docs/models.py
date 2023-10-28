from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

document = Table(
    "document",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", Integer, nullable=False),
    Column("name", String, nullable=False),
    Column("content", String, nullable=False),
)
