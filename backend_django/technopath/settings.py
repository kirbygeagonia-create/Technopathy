import os
from pathlib import Path
from decouple import config, UndefinedValueError

BASE_DIR = Path(__file__).resolve().parent.parent

# In production, SECRET_KEY MUST be set via .env — no insecure fallback.
# In development (DEBUG=True), auto-generate a random key if not set.
_debug = config('DEBUG', default=False, cast=bool)
try:
    SECRET_KEY = config('SECRET_KEY')
except UndefinedValueError:
    if _debug:
        import secrets
        SECRET_KEY = secrets.token_urlsafe(50)
        print('[WARNING] SECRET_KEY not set — using auto-generated dev key. Set SECRET_KEY in .env for production.')
    else:
        raise RuntimeError('SECRET_KEY environment variable is required in production. Set it in your .env file.')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'apps.users',
    'apps.facilities',
    'apps.rooms',
    'apps.navigation',
    'apps.chatbot',
    'apps.notifications',
    'apps.feedback',
    'apps.core',
    'apps.announcements',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'technopath.urls'

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

WSGI_APPLICATION = 'technopath.wsgi.application'

# Database - PostgreSQL in production, SQLite locally
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production — use PostgreSQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
elif not DEBUG:
    # Safety guard: refuse to start in production without a real database.
    # Render's free SQLite would be wiped on every restart — all data lost.
    raise RuntimeError(
        '\n\n'
        '  DATABASE_URL is not set and DEBUG=False.\n'
        '  This means the app is running in production without a database.\n'
        '  Create a PostgreSQL instance in Render and set DATABASE_URL.\n'
        '  Never use SQLite in production on Render (it is wiped on restart).\n'
    )
else:
    # Local development — SQLite is fine
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'technopath.db',
        }
    }

AUTH_USER_MODEL = 'users.AdminUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '120/minute',
    },
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:5173',
    'http://localhost:4173',
    'http://localhost:4174',
    'http://localhost:4175',
    'http://localhost:4176',
    'http://localhost:4177',
    # Render production URLs - include all possible variations
    'https://technopath-frontend.onrender.com',
    'https://technopath-frontend-or73.onrender.com',
    'https://technopath-backend.onrender.com',
    'https://technopath-backend-or73.onrender.com',
]
CORS_ALLOW_CREDENTIALS = True

# Allow additional origins from environment variable (comma-separated)
_cors_env = config('CORS_ALLOWED_ORIGINS', default='')
if _cors_env:
    for origin in _cors_env.split(','):
        origin = origin.strip()
        if origin and origin not in CORS_ALLOWED_ORIGINS:
            CORS_ALLOWED_ORIGINS.append(origin)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True
