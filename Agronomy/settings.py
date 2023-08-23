"""
Django settings for Agronomy project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import sys
import os

import Agronomy.middleware
from . import sensitive
from pathlib import Path
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = sensitive.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = sensitive.DEBUG

ALLOWED_HOSTS = sensitive.ALLOWED_HOSTS
ALLOWED_DOMAIN = sensitive.ALLOWED_DOMAIN
CSRF_TRUSTED_ORIGINS = sensitive.CSRF_TRUSTED_ORIGINS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'channels',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'pages',
    'accounts',
    'managements',
]

# Auth User Model
AUTH_USER_MODEL = 'accounts.Account'

AUTHENTICATION_BACKENDS = [
    'accounts.backends.CustomModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = "none"
#ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USER_DISPLAY = "accounts.utils.custom_user_display"
LOGIN_REDIRECT_URL = '/'

SITE_ID = 2 if os.environ['PRODUCTION'] == 'Yes' else 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = 'accounts.forms.CustomDefaultSocialAccountAdapter'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Agronomy.middleware.SessionCheckerMiddleware',
    'Agronomy.middleware.PreventGoogleOauthMiddleware',
]

ROOT_URLCONF = 'Agronomy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Agronomy.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'Agronomy.wsgi.application'
ASGI_APPLICATION = 'Agronomy.asgi.application'

CHANNEL_LAYERS = sensitive.CHANNEL_LAYERS

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = sensitive.DATABASES


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# For Bengali words support
DEFAULT_CHARSET = 'utf-8'

LANGUAGE_CODE = 'bn'

TIME_ZONE = 'Asia/Dacca'

USE_I18N = True

USE_TZ = True

# Multilanguage

USE_L10N = True

LANGUAGES = (
    ('bn', _('Bengali')),
    ('en', _('English')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = (str(BASE_DIR.joinpath('staticfiles')), str(BASE_DIR.joinpath('mediafiles')))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

# Logs
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'debug.log'),
            'formatter': 'verbose',
            'mode': 'w',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'info.log'),
            'formatter': 'verbose',
            'mode': 'w',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'warning.log'),
            'formatter': 'verbose',
            'mode': 'w',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
            'formatter': 'verbose',
            'mode': 'w',
        },
        'critical_file': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'critical.log'),
            'formatter': 'verbose',
            'mode': 'w',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'debug_file', 'info_file', 'warning_file', 'error_file', 'critical_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 10mb = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Session age in seconds for 2 days
SESSION_COOKIE_AGE = 60 * 60 * 24 * 2

# Google reCAPTCHA
# v2
RECAPTCHA_V2_SITE_KEY = sensitive.RECAPTCHA_V2_SITE_KEY
RECAPTCHA_V2_SECRET_KEY = sensitive.RECAPTCHA_V2_SECRET_KEY

# v3
RECAPTCHA_V3_SITE_KEY = sensitive.RECAPTCHA_V3_SITE_KEY
RECAPTCHA_V3_SECRET_KEY = sensitive.RECAPTCHA_V3_SECRET_KEY

# File based Email Configuration
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = BASE_DIR / 'emails'

# SMTP Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = sensitive.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = sensitive.EMAIL_HOST_PASSWORD

