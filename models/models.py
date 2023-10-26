from sqlalchemy import MetaData, Integer, String, Table, Column

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id",Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("password", String, nullable=False),
)