from .base import *

# DJANGO_SETTINGS_MODULE="soccerstreams.settings.production"

ALLOWED_HOSTS = ['*'] # soccer-streams02.herokuapp.com

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'djx4q2y-yyvjozclbw4*t1w!ph#l2om^24gc(j$09%njvjbg++'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9tuc6o4fjvk70',
        'USER': 'ggwunygmlvyamx',
        'PASSWORD': 'e37ed4fd3707bdc664815cd2daf21ab2ea106a6e225fa665fddafa185f16625d',
        'HOST': 'ec2-23-21-147-71.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}