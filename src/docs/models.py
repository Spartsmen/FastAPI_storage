from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


metadata = MetaData()

document = Table(
    "document",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", Integer, nullable=False),
    Column("name", String, nullable=False),
    Column("content", String, nullable=False),
)
referrals = Table(
    "referrals",
    metadata,
    Column("source_id", Integer, nullable=True),
    Column("target_id",Integer, ForeignKey("document.id")),
)
