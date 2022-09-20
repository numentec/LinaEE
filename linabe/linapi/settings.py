"""
Django settings for linapi project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from os import environ
from datetime import timedelta
# from .permissions import CustomDjangoModelPermissions

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("SECRET_KEY")

DEBUG = (environ.get("APP_DEBUG", True) == '1')

ALLOWED_HOSTS = ['*']
# USE_X_FORWARDED_HOST = True

# Application definition
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'ckeditor',

    # Numen Apps
    'apps.core',
    'apps.inv',
    'apps.linabi',
    'apps.wms',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'linapi.wsgi.application'

# Database
DATABASE_ROUTERS = ['apps.core.routers.DbRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ.get("DB_NAME"),
        'USER': environ.get("DB_USER"),
        'PASSWORD': environ.get("DB_USER_PW"),
        'HOST': environ.get("DB_HOST"),
        'PORT': environ.get("DB_PORT"),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'extdb1': {
        'ENGINE': environ.get('EXTDB1_ENGINE'),
        'NAME': environ.get('EXTDB1_NAME'),
        'USER': environ.get('EXTDB1_USER'),
        'PASSWORD': environ.get('EXTDB1_USER_PW'),
        'HOST': environ.get('EXTDB1_HOST'),
        #'HOST': '201.218.202.45',
        'PORT': environ.get('EXTDB1_PORT'),
    },
}

# Password validation
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/day',
        'user': '1000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.HeaderLimitOffsetPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    # 'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=45),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': environ.get("SECRET_KEY"),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=45),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Internationalization
LANGUAGE_CODE = environ.get("LOC_LG").lower().replace('/', '-')
#LANGUAGE_CODE = 'es-pa'

USE_TZ = True
TIME_ZONE = environ.get("LOC_TZ")
# TIME_ZONE = 'America/Panama'

USE_I18N = True

USE_L10N = True

AUTH_USER_MODEL = 'core.User'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = '/linabe/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/linabe/media/'

# IPWARE_META_PRECEDENCE_ORDER = (
#     'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',  # <client>, <proxy1>, <proxy2>
#     'HTTP_CLIENT_IP',
#     'HTTP_X_REAL_IP',
#     'HTTP_X_FORWARDED',
#     'HTTP_X_CLUSTER_CLIENT_IP',
#     'HTTP_FORWARDED_FOR',
#     'HTTP_FORWARDED',
#     'HTTP_VIA',
#     'REMOTE_ADDR',
# )

# PROXY_COUNT = 1
# PROXY_TRUSTED = ['192.168.15.11']
# PROXY_COUNT = environ.get("PROXY_COUNT")
# PROXY_TRUSTED = environ.get("PROXY_TRUSTED")
