from peewee import SqliteDatabase, Model, CharField, DateTimeField

__author__ = 'afox'
database = SqliteDatabase("boxoffice/movies.db")


class BaseModel(Model):
    class Meta:
        database = database


class Movie(BaseModel):
    date_added = DateTimeField()
    title = CharField()
    audience_score = CharField()
    year = CharField()
    mpaa_rating = CharField()
    synopsis = CharField()
    link = CharField()

    class Meta:
        order_by = ('-date_added',)
