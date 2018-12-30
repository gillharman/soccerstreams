from .base import *

# DJANGO_SETTINGS_MODULE="soccerstreams.settings.production"

ALLOWED_HOSTS = ['soccer-streams02.herokuapp.com'] # soccer-streams02.herokuapp.com

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default' : {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}