"""
Django settings for config project.
"""

from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================================
# SEGURIDAD
# ========================================

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['*']


# ========================================
# APLICACIONES
# ========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',  # Para Azure Blob Storage
    'cv',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ========================================
# BASE DE DATOS
# ========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ========================================
# VALIDACIÓN DE CONTRASEÑAS
# ========================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ========================================
# INTERNACIONALIZACIÓN
# ========================================

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True


# ========================================
# ARCHIVOS ESTÁTICOS (CSS, JS, BOOTSTRAP)
# Archivos del código fuente que NO cambian
# ========================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Directorio adicional para archivos estáticos (si lo usas)
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


# ========================================
# ARCHIVOS MEDIA (SUBIDOS POR USUARIOS)
# Certificados, fotos, PDFs, imágenes de productos
# ALMACENADOS EN: AZURE BLOB STORAGE
# ========================================

# Backend para almacenar archivos media
# ==============================
# STORAGE (LOCAL vs AZURE)
# ==============================

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Credenciales de Azure (desde .env)
AZURE_ACCOUNT_NAME = config('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = config('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = config('AZURE_CONTAINER', default='media')

# Dominio de Azure
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# URL pública de los archivos
# Ejemplo: https://cvjeanpi21.blob.core.windows.net/media/certificados/cert1.jpg
MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/"


# ⚠️ NO definir MEDIA_ROOT cuando usas Azure
# MEDIA_ROOT solo se usa para almacenamiento LOCAL


# ========================================
# CONFIGURACIÓN AVANZADA DE AZURE
# ========================================

# Usar HTTPS
AZURE_SSL = True

# Configuración de conexión
AZURE_UPLOAD_MAX_CONN = 2
AZURE_TIMEOUT = 20
AZURE_MAX_MEMORY_SIZE = 2 * 1024 * 1024  # 2MB

# Headers HTTP para archivos subidos
AZURE_OBJECT_PARAMETERS = {
    'cache_control': 'max-age=86400',  # Cache por 1 día
}


# ========================================
# CONFIGURACIÓN ADICIONAL
# ========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'