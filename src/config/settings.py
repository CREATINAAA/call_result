import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True if os.environ.get("DEBUG") == "True" else False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(',')

AMO_DAIGO_INTEGRATION_SUBDOMAIN = os.environ.get("AMO_DAIGO_INTEGRATION_SUBDOMAIN")
AMO_DAIGO_INTEGRATION_CLIENT_SECRET = os.environ.get("AMO_DAIGO_INTEGRATION_CLIENT_SECRET")
AMO_DAIGO_INTEGRATION_CLIENT_ID = os.environ.get("AMO_DAIGO_INTEGRATION_CLIENT_ID")
AMO_DAIGO_INTEGRATION_CODE = os.environ.get("AMO_DAIGO_INTEGRATION_CODE")
AMO_DAIGO_INTEGRATION_REDIRECT_URI = os.environ.get("AMO_DAIGO_INTEGRATION_REDIRECT_URI")

AMO_MOLOKO_INTEGRATION_SUBDOMAIN = os.environ.get("AMO_MOLOKO_INTEGRATION_SUBDOMAIN")
AMO_MOLOKO_INTEGRATION_CLIENT_SECRET = os.environ.get("AMO_MOLOKO_INTEGRATION_CLIENT_SECRET")
AMO_MOLOKO_INTEGRATION_CLIENT_ID = os.environ.get("AMO_MOLOKO_INTEGRATION_CLIENT_ID")
AMO_MOLOKO_INTEGRATION_CODE = os.environ.get("AMO_MOLOKO_INTEGRATION_CODE")
AMO_MOLOKO_INTEGRATION_REDIRECT_URI = os.environ.get("AMO_MOLOKO_INTEGRATION_REDIRECT_URI")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'leadtransfer',
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "WantresultIncomingLeads.log"
        },
    },
    "loggers": {
        "leadtransfer": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  os.environ.get("POSTGRES_DB"),
        'USER':  os.environ.get("POSTGRES_USER"),
        'PASSWORD':  os.environ.get("POSTGRES_PASSWORD"),
        'HOST':  os.environ.get("POSTGRES_HOST"),
        'PORT':  os.environ.get("POSTGRES_PORT", 5432),
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

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_RECEIVERS = os.environ.get("EMAIL_RECEIVERS").split(",")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'
