"""Django settings."""

import os
import sys

import environ
import requests
import urllib3

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2

env_file = str(BASE_DIR.path('.env'))
if os.path.exists(env_file):
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See config/settings.py for more information.')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=os.path.exists(env_file))

ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', cast=str.split, default=[])
ALLOWED_HOSTS.append('127.0.0.1')  # Allow health check inside container

# Allow requests to AWS EC2 private IP i.e. load balancer health checks
# https://gist.github.com/dryan/8271687
EC2_PRIVATE_IP = None
try:
    _response = requests.get(
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        timeout=0.01,
    )
    EC2_PRIVATE_IP = _response.text
    if EC2_PRIVATE_IP:
        ALLOWED_HOSTS.append(EC2_PRIVATE_IP)
except requests.exceptions.RequestException:
    pass

APP_COMMIT = env("APP_COMMIT", default=None)
APP_ENVIRONMENT = env("APP_ENVIRONMENT", default=None)
APP_RELEASE = env("APP_RELEASE", default=None)
SENTRY_DSN = env("SENTRY_DSN", default=None) if not sys.stdin.isatty() else None

PROJECT_APPS = [
    'bloob',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'health_check',
    'health_check.db',

    # Mintel apps
    'gatekeeper',
] + PROJECT_APPS


if SENTRY_DSN:
    INSTALLED_APPS.append("raven.contrib.django.raven_compat")
    RAVEN_CONFIG = {
        "dsn": SENTRY_DSN,
        "environment": APP_ENVIRONMENT,
        "release": APP_RELEASE,
        "commit": APP_COMMIT,
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(message)s',
        },
        'verbose': {
            'format': ('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(funcName)s: '
                       '%(message)s'),
        },
    },
    'loggers': {
        '': {  # root
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'urllib3': {
            'handlers': ['console'],
            'level': 'WARNING',
        }
    },
    'handlers': {
        'console': {
            'level': ('DEBUG' if DEBUG else 'WARNING'),
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'gatekeeper.middleware.GatekeeperAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.path(app, 'templates') for app in PROJECT_APPS],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': env.db(
        'DJANGO_DATABASE_URL',
        default='sqlite:///' + str(BASE_DIR.path('db.sqlite3')),
    ),
}

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = ['gatekeeper.auth.GatekeeperAuthBackend']
GK_EXEMPT_URLS = ['health_check_home']
GK_UPDATE_BASE_URL = True

GK_ROLES = [
    'my_role',
]

STATIC_ROOT = env('DJANGO_STATIC_ROOT', default=str(BASE_DIR.path('static')))
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'gatekeeper.static.GKStaticFilesStorage'
