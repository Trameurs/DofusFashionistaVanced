# Copyright (C) 2020 The Dofus Fashionista
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
Django settings for fashionsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json
import platform
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Define the paths for Linux and Windows
if platform.system() == 'Windows':
    CONFIG_DIR = os.path.join(os.environ['APPDATA'], 'fashionista')
else:
    CONFIG_DIR = '/etc/fashionista'

# Use the appropriate paths for the current platform
with open(os.path.join(CONFIG_DIR, 'gen_config.json'), 'r') as f:
    GEN_CONFIGS = json.loads(f.read())
    
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = GEN_CONFIGS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
with open(os.path.join(CONFIG_DIR, 'debug_mode')) as f:
    content = f.read().strip()
    DEBUG = (content == 'True')
    print('DEBUG: %s' % DEBUG)

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ['fashionistavanced.com', 'www.fashionistavanced.com', '16.171.215.36']

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'static_s3',
    'chardata',
    'sslserver',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.request',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
   'social_core.backends.facebook.FacebookOAuth2',
   'social_core.backends.google.GoogleOAuth2',
   'social_core.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

# Uncomment to minify even in DEBUG mode.
# HTML_MINIFY = True

ROOT_URLCONF = 'fashionsite.urls'

WSGI_APPLICATION = 'fashionsite.wsgi.application'

LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GEN_CONFIGS['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GEN_CONFIGS['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type':'offline'}
SOCIAL_AUTH_SESSION_EXPIRATION = False

SOCIAL_AUTH_FACEBOOK_KEY = GEN_CONFIGS['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = GEN_CONFIGS['SOCIAL_AUTH_FACEBOOK_SECRET']


USE_MYSQL = True
if USE_MYSQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'fashionista',
            'USER': GEN_CONFIGS['mysql_USER'],
            'PASSWORD': GEN_CONFIGS['mysql_PASSWORD'],
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('pt', 'Portuguese'),
    ('de', 'Deutsch'),
)

LOCALE_PATHS = (os.path.join(os.path.dirname(os.path.abspath(__file__)), '../locale'),)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_FILES_BUCKET = 'fashionistavanced'
with open(os.path.join(CONFIG_DIR, 'serve_static')) as f:
    serve_static = True #f.read().startswith('True')
    if not serve_static or not DEBUG:
        #STATIC_URL = 'https://fashionistavanced.s3.eu-north-1.amazonaws.com/'
        #ALLOWED_HOSTS = ['fashionistavanced.com', 'www.fashionistavanced.com']
        STATIC_ROOT = '/tmp/statictemp'
        STATIC_URL = '/static/'
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    else:
        STATIC_ROOT = '/tmp/statictemp'
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        #'logfile': {
        #    'level':'DEBUG',
        #    'class':'logging.handlers.RotatingFileHandler',
        #    'filename': '/tmp/fashionista_log.txt',
        #    'maxBytes': 50000,
        #    'backupCount': 2,
        #    'formatter': 'standard',
        #},
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'MYAPP': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

CACHES = { 
  'default' : { 
     'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache', 
     'LOCATION' : '127.0.0.1:11211',
     'TIMEOUT': 600,
     'CULL_FREQUENCY': 3
  }
}

EMAIL_USE_TLS = GEN_CONFIGS['EMAIL_USE_TLS']
EMAIL_HOST = GEN_CONFIGS['EMAIL_HOST']
EMAIL_HOST_USER = GEN_CONFIGS['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = GEN_CONFIGS['EMAIL_HOST_PASSWORD']
EMAIL_PORT = GEN_CONFIGS['EMAIL_PORT']

SITE_VERSION = '3.0.45.37'

EXPERIMENTS = {
    'COMPARE_SETS': True,
    'TRANSLATION': True,
    'WEAPONS': True,
    'ITEM_LINKS': True,
}

DEFAULT_THEME = 'lighttheme'