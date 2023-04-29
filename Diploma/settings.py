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

import admin_panel

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6v-km5ek+98hkvq^wf!*h1yiyg6lqeknkixqj%m^-j-#4k@y+u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

GOOGLE_MAPS_API_KEY = 'AIzaSyBCATtzO_qe6Iv19vT0x0eymL7DKuFzotI'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'danilgusin17@gmail.com'
EMAIL_HOST_PASSWORD = 'hdbfokyujlwegcxd'
DEFAULT_FROM_EMAIL = 'danilgusin17@gmail.com'
DEFAULT_TO_EMAIL = 'Your email'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Application definition
"""Программными ядрами библиотек Django REST framework и django-cors-headers
являются приложения rest framework и corsheaders соответственно. Их необходимо
добавить в список зарегистрированных в проекте """
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'kino_app.apps.KinoAppConfig',
    'admin_panel.apps.AdminPanelConfig',
    'django_test_app.apps.DjangoTestAppConfig',
    'user.apps.UserConfig',
    'crispy_forms',
    'qr_code',
    'django.contrib.postgres',
    'rest_framework',
    "corsheaders",
    "django_bootstrap5",
]
AUTH_USER_MODEL = 'admin_panel.Account'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

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
            'libraries':{
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
        'NAME': 'kino_cms',
        'USER': 'postgres',
        'PASSWORD': 'buzaho4114',
        'HOST': '127.0.0.1',
        'PORT': 5432

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

USE_TZ = True

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
MEDIA_URL = '/media/'
