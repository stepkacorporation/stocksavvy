"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os

from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.getenv('DEBUG', 'False')) == 'True'

ALLOWED_HOSTS = str(os.getenv('ALLOWED_HOSTS')).split()

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'debug_toolbar',

    'rest_framework',
    'corsheaders',
    
    'crispy_forms',
    'crispy_bootstrap5',

    'apps.accounts.apps.AccountsConfig',
    'apps.stocks.apps.StocksConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = str(os.getenv('INTERNAL_IPS')).split()

CORS_ALLOWED_ORIGINS = str(os.getenv('CORS_ALLOWED_ORIGINS')).split()
CSRF_TRUSTED_ORIGINS = str(os.getenv('CSRF_TRUSTED_ORIGINS')).split()

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# CRYSPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.getenv('DB_NAME')),
        'USER': str(os.getenv('DB_USER')),
        'PASSWORD': str(os.getenv('DB_PASSWORD')),
        'HOST': str(os.getenv('DB_HOST')),
        'PORT': str(os.getenv('DB_PORT')),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = 'stocks'
ACCOUNT_ACTIVATION_DAYS = 30

# EMAIL
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_PORT = str(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = str(os.getenv('EMAIL_USE_TLS', 'False')) == 'True'
DEFAULT_FROM_EMAIL = str(os.getenv('DEFAULT_FROM_EMAIL'))

# ASYNC TASK
REDIS_BROKER_HOST = str(os.getenv('REDIS_BROKER_HOST'))
REDIS_BROKER_PORT = str(os.getenv('REDIS_BROKER_PORT'))
BROKER_URL = 'redis://' + REDIS_BROKER_HOST + ':' + REDIS_BROKER_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_BROKER_HOST + ':' + REDIS_BROKER_PORT + '/0'
CELERY_TIMEZONE = TIME_ZONE

# CACHE
REDIS_CACHE_HOST = str(os.getenv('REDIS_CACHE_HOST'))
REDIS_CACHE_PORT = str(os.getenv('REDIS_CACHE_PORT'))
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://' + REDIS_CACHE_HOST + ':' + REDIS_CACHE_PORT + '/0',
    }
}

# LOGGING
LOGGING_DIR = BASE_DIR / '../logs'
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] {processName}/{threadName} {module}.{funcName}:{lineno} -> {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{asctime}] [{levelname}] -> {message}',
            'style': '{',
        },
    },
    'handlers': {
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR / 'celery.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        'stocks': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR / 'stocks.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['celery', 'console'],  # They are specified in the config.celery
            'level': 'INFO',
            'propagate': True,
        },
        'stocks': {
            'handlers': ['stocks', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}