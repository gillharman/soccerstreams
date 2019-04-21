from .base import *

# DJANGO_SETTINGS_MODULE="soccerstreams.settings.production"

ALLOWED_HOSTS = ['soccer-streams02.herokuapp.com'] # soccer-streams02.herokuapp.com
# ALLOWED_HOSTS = ['*']

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3c592kev84un',
        'USER': 'rpsjqjgwniikyi',
        'PASSWORD': '18b25f3eda9c069b14b5b20faaa3310201ba187efceb1098e545044f2cbe91d9',
        'HOST': 'ec2-54-235-178-189.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}