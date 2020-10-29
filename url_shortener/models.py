from peewee import SqliteDatabase, Model, CharField, IntegerField, DatabaseProxy

from config import DB_NAME


database = SqliteDatabase(DB_NAME)


class Url(Model):
    url = CharField()
    views = IntegerField(default=0)

    class Meta:
        database = database


def create_tables():
    with database:
        database.create_tables([Url])
