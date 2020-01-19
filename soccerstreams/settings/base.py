"""
Django settings for soccerstreams project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
# from google.oauth2 import service_account

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


SECRET_KEY = 'secret'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'streamablematches',
    'matches',
    'teams',
    'leagues',
    'lineups',
    'logs',
    'users',
    'gunicorn',
    'django_cron',
    'django_user_agents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

CRON_CLASSES = [
    'crons.crons.StreamScraper',
    'crons.crons.GetGames',
    'crons.crons.GetLineups',
    'crons.crons.Cleanup'
]

ROOT_URLCONF = 'soccerstreams.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'soccerstreams.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static_collected')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

# MEDIA_ROOT = os.path.join(PROJECT_DIR, 'users/media/')

# MEDIA_URL = 'users/media/'

AUTH_USER_MODEL = 'users.User'

########################
# API RELATED SETTINGS #
########################

REQUEST_HEADERS = {
    "reddit": "{'user_agent': 'laptop:soccerStreams:v 0.1'}",
    "footballApi": "{'x-auth-token': '335ffd5c439f4d3ea4f5ade02de7b207'}",
    "rotowire": "{'user_agent': 'pc'}"
}

FOOTBALL_API_BASE_URL = "https://api.football-data.org/v2"

FOOTBALL_API_URLS = {
    "competitions": "/competitions",
    "competitionSeasons": "/competitions/%s",
    "teams": "/competitions/%s/teams",
    "matches": "/competitions/%s/matches"
}

REDDIT_BASE_URL = "http://www.reddit.com/r/"

REDDIT_API_URL = {
    "soccerstreams": "soccerstreams/.json"
}

ROTOWIRE_BASE_URL = "https://www.rotowire.com/soccer/lineups.php"

ROTOWIRE_LEAGUE_URLS = {
    "PL": "",
    "FL1": "?league=FRAN",
    "PD": "?league=LIGA",
    "SA": "?league=SERI",
    "BL1": "?league=BUND",
    "MLS": "?league=MLS",
    "CL": "?league=UCL",
    "LMX": "?league=LMX"
}
