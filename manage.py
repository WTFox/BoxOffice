import argparse

from peewee import OperationalError

from boxoffice.models import Movie


def clearTable(parsed_args):
    try:
        Movie.drop_table()
    except OperationalError:
        Movie.create_table()


def recentlyAdded(parsed_args):
    for movie in Movie.select().order_by(-Movie.date_added)[:10]:
        print(movie.audience_score, movie.title)


parser = argparse.ArgumentParser()

parser.add_argument('--clear-table', dest='action', action='store_const', const=clearTable)
parser.add_argument('--recently-added', dest='action', action='store_const', const=recentlyAdded)

parsed_args = parser.parse_args()
if parsed_args.action is None:
    parser.parse_args(['-h'])
parsed_args.action(parsed_args)