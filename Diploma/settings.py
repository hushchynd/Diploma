"""
Django settings for Diploma project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

from django.db import models

import admin_panel

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6v-km5ek+98hkvq^wf!*h1yiyg6lqeknkixqj%m^-j-#4k@y+u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['https://diploma-production-a075.up.railway.app/']
GOOGLE_MAPS_API_KEY = 'AIzaSyBCATtzO_qe6Iv19vT0x0eymL7DKuFzotI'
CSRF_TRUSTED_ORIGINS = ['https://diploma-production-a075.up.railway.app']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dhushchyn@gmail.com'
EMAIL_HOST_PASSWORD = 'mfpxzbsjatijcboa'
DEFAULT_FROM_EMAIL = 'dhushchyn@gmail.com'
DEFAULT_TO_EMAIL = 'Your email'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_BROKER_URL = "rediss://:p935eb5f0097da33d3517959945c79180f38c8a05ea62bdac9c4e82bf405e51e5@ec2-52-71-63-156.compute-1.amazonaws.com:13730"
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = "rediss://:p935eb5f0097da33d3517959945c79180f38c8a05ea62bdac9c4e82bf405e51e5@ec2-52-71-63-156.compute-1.amazonaws.com:13730"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Application definition
"""Программными ядрами библиотек Django REST framework и django-cors-headers
являются приложения rest framework и corsheaders соответственно. Их необходимо
добавить в список зарегистрированных в проекте """
INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'kino_app.apps.KinoAppConfig',
    'admin_panel.apps.AdminPanelConfig',
    'user.apps.UserConfig',
    'django.contrib.postgres',
    "django_bootstrap5",
    "django_google_maps",

]
AUTH_USER_MODEL = 'admin_panel.Account'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]
ROOT_URLCONF = 'Diploma.urls'

"""
чтобы разрешить обработку запросов, приходящих с любых доменов,
но только к тем путям, что включают префикс api, следует добавить в модуль
settings.py пакета конфигурации такие выражения:
"""
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'A/api/.*$'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'kino_app.middlewares.baseView',

            ],
            'libraries': {
                'file_filters': 'admin_panel.templatetags.file_filters'
            }
        },
    },
]

# LOGIN_REDIRECT_URL = 'main'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

WSGI_APPLICATION = 'Diploma.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["PGDATABASE"],
        'USER': os.environ["PGUSER"],
        'PASSWORD': os.environ["PGPASSWORD"],
        'HOST': os.environ["PGHOST"],
        'PORT': os.environ["PGPORT"],
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
LOGIN_URL = 'signin'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('Английский')),
    ('ru', _('Русский')),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

import django_on_heroku

django_on_heroku.settings(locals())
