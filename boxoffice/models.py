from peewee import SqliteDatabase, Model, CharField, DateTimeField, OperationalError

__author__ = 'afox'
database = SqliteDatabase("movies.db")


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


if __name__ == "__main__":
    # Movie.drop_table()

    try:
        Movie.create_table()
    except OperationalError:
        print("Movie table already exists!")
