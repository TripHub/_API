from .common import *


# turn DEBUG off so tests run faster
DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
