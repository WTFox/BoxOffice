import argparse

from peewee import OperationalError

from boxoffice.models import Movie


def clearTable(parsed_args):
    """
    Clears the table Movies

    :param parsed_args:
    :return:
    """

    try:
        Movie.drop_table()
    except OperationalError:
        Movie.create_table()

    return


def createTable(parsed_args):
    """
    Creates the table Movies

    :param parsed_args:
    :return:
    """

    try:
        Movie.create_table()
    except OperationalError:
        print("Movie table already exists!")

    return


def recentlyAdded(parsed_args):
    """
    Displays the last 10 movies added to Couchpotato via this script.

    :param parsed_args:
    :return:
    """

    print("\nThe last 10 movies added were: \n")
    for movie in Movie.select()[:10]:
        print("{}\t{}%\t{}".format(movie.date_added, movie.audience_score, movie.title))

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--clear-table', dest='action', action='store_const', const=clearTable)
    parser.add_argument('--create-table', dest='action', action='store_const', const=createTable)
    parser.add_argument('--recently-added', dest='action', action='store_const', const=recentlyAdded)

    parsed_args = parser.parse_args()
    if parsed_args.action is None:
        parser.parse_args(['-h'])

    parsed_args.action(parsed_args)