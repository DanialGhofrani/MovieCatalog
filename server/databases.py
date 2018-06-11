import os
from peewee import PostgresqlDatabase


class PostgresDB(object):
    instance = None

    @classmethod
    def initialize_postgres(cls):
        if os.environ['ENV'] == 'TEST':
            PostgresDB.instance = PostgresqlDatabase(
                'movie_catalogue_test',
                user='dannyboy',
                password='fake_pwd',
                host='0.0.0.0', port=5432
            )
        else:
            PostgresDB.instance = PostgresqlDatabase(
                'movie_catalogue',
                user='dannyboy',
                password='fake_pwd',
                host='0.0.0.0', port=5432
            )

    @classmethod
    def get_postgres(cls):
        if PostgresDB.instance is None:
            PostgresDB.initialize_postgres()
        return PostgresDB.instance
