import logging

from peewee import OperationalError

from boxoffice import boxoffice as b
from boxoffice.models import Movie


# create logger with 'spam_application'
logger = logging.getLogger('boxoffice_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('boxoffice.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Movie.drop_table()

try:
    Movie.create_table()
except OperationalError:
    logger.info("Movie table already exists!")

logger.info("Boxoffice starting")
b.getMovies()
logger.info("All done")