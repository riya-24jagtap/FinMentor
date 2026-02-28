# fintechsnap/settings.py

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
  # temporary, change later

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-m8_k#e9@ioe^k0vd3pq89)8)o!&imagc25g)b%uu20l+=#d!j('

DEBUG = False


ALLOWED_HOSTS = ['*']
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fintechsnap.analysis',
    'fintechsnap.predictor',
    'fintechsnap.financeapp.apps.FinanceappConfig',
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
]

ROOT_URLCONF = 'fintechsnap.urls'


# ---------------------------
#      TEMPLATE SETTINGS
# ---------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "fintechsnap" / "templates",   # main templates folder
            BASE_DIR / "templates",                   # optional project-level templates folder
        ],
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


WSGI_APPLICATION = 'fintechsnap.wsgi.application'


# ---------------------------
#         DATABASE
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ---------------------------
#   PASSWORD VALIDATION
# ---------------------------
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


# ---------------------------
#   INTERNATIONALIZATION
# ---------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'   # change to 'Asia/Kolkata' if you want

USE_I18N = True
USE_TZ = True


# ---------------------------
#     STATIC & MEDIA FILES
# ---------------------------

# URL for static files
STATIC_URL = '/static/'

# Where your static files actually live during development
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Folder Django will collect static files into for production
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'landing'       # after login => /
LOGOUT_REDIRECT_URL = 'landing'      # after logout => /
