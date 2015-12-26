from __future__ import print_function
import datetime
import urllib.parse
import logging

import requests

from . import config
from .models import Movie
from .notifiers import PushBullet


__author__ = 'afox'

PB_API_KEY = config.PB_API_KEY
CP_API_KEY = config.CP_API_KEY
CP_URL = config.CP_URL.format(CP_API_KEY)
RT_API_KEY = config.RT_API_KEY
RT_URL = config.RT_URL.format(RT_API_KEY)

logger = logging.getLogger('boxoffice_logger')


def getMovies(defaultScore=60, defaultQuantity=10):
    """
    Grabs the box office movies from Rottentomatoes.com and adds the movies with an audience score higher than defaultScore to CouchPotato.

    :param defaultScore: Score in percent out of 100. e.g. Any movie over 60%
    :param defaultQuantity: How many movies do we want to process. Max is 25.
    :return:
    """

    today = datetime.date.today()
    added_movies = [m.title for m in Movie.select(Movie.title)]
    rtData = requests.get(RT_URL).json()

    for x in range(defaultQuantity):
        movie = dict(
            title=rtData["movies"][x]["title"],
            year=rtData["movies"][x]["year"],
            audience_score=rtData["movies"][x]["ratings"]["audience_score"],
            synopsis=rtData["movies"][x]["synopsis"][:500] + '...',
            mpaa_rating=rtData["movies"][x]["mpaa_rating"],
            link=rtData["movies"][x]["links"]["alternate"],
            date_added=today
        )

        if movie['audience_score'] > defaultScore and movie["title"] not in added_movies:
            logger.info("Adding {} to Couchpotato".format(movie["title"]))
            movie_record = Movie(**movie)
            movie_record.save()

            addMovieToCP(movie)
            sendNotification(movie)

    return


def addMovieToCP(movie):
    movieURLTitle = urllib.parse.quote(movie['title'])
    movieSearch = "{}movie.search?q={}".format(CP_URL, movieURLTitle)
    jsonData = requests.get(movieSearch).json()
    movieID = jsonData["movies"][0]["imdb"]

    requests.get(CP_URL + "movie.add/",
                 params={'identifier': movieID})

    return


def sendNotification(movie):
    pb = PushBullet(PB_API_KEY)
    status = "Added " + movie['title']
    msg = movie['title'] + " - " + str(movie['audience_score']) + "%\n" + movie['synopsis'][:140]
    pb.pushNote(title=status, body=msg)

    return


if __name__ == "__main__":
    pass
