"""
Django settings for Document Summarizer project.

This configuration file contains all the settings needed to run the document
summarization application. Most sensitive settings are loaded from environment
variables for security and flexibility across different deployment environments.
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings - should be overridden in production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-insecure-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Hosts allowed to access this application
ALLOWED_HOSTS = [h.strip() for h in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Application definition - Django apps and our custom apps
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps for API and authentication
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    
    # Our custom applications
    'accounts',        # User authentication and management
    'documents',       # Document upload and text extraction
    'summarization',   # AI summarization engine
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'summarizer_backend.urls'

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

WSGI_APPLICATION = 'summarizer_backend.wsgi.application'
ASGI_APPLICATION = 'summarizer_backend.asgi.application'

USE_POSTGRES = os.getenv('USE_POSTGRES', 'False').lower() == 'true'

if USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'summarizer'),
            'USER': os.getenv('POSTGRES_USER', 'summarizer_user'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Added for DRF browsable API
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()]
CORS_ALLOW_ALL_ORIGINS = not CORS_ALLOWED_ORIGINS

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

# Celery
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Summarization configuration
SUMMARIZATION_MODEL_NAME = os.getenv('SUMMARIZATION_MODEL_NAME', 't5-small')
SUMMARY_SHORT_MAX_LEN = int(os.getenv('SUMMARY_SHORT_MAX_LEN', '60'))
SUMMARY_SHORT_MIN_LEN = int(os.getenv('SUMMARY_SHORT_MIN_LEN', '15'))
SUMMARY_DETAILED_MAX_LEN = int(os.getenv('SUMMARY_DETAILED_MAX_LEN', '180'))
SUMMARY_DETAILED_MIN_LEN = int(os.getenv('SUMMARY_DETAILED_MIN_LEN', '60'))

# Document extraction limits
MAX_DOCUMENT_SIZE_MB = int(os.getenv('MAX_DOCUMENT_SIZE_MB', '25'))  # Hard cap before forcing async
MAX_EXTRACT_CHAR = int(os.getenv('MAX_EXTRACT_CHAR', '60000'))  # Truncate extracted text to this length
AUTO_SUMMARY_MAX_CHAR = int(os.getenv('AUTO_SUMMARY_MAX_CHAR', '40000'))  # Above this we may defer to async later
