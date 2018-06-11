from peewee import (
    Model,
    TextField
)
from databases import PostgresDB

pg_db = PostgresDB.get_postgres()


class BaseModel(Model):
    class Meta:
        database = pg_db

    uuid = TextField(null=False)
