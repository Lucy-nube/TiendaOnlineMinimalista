from pathlib import Path
import os
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'asdfg12345hjkl67890yeuy356q3572ef27ef6eftfdfustfeu'
)

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    'tareadjango.onrender.com'
]

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # APIs y Almacenamiento (Cloudinary storage debe ir antes de cloudinary)
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',

    # Apps
    'accounts',
    'product',
    'order',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Debe ir después de Security
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# TEMPLATES
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
                'product.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE (POSTGRESQL RENDER)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

# CSRF - Importante para evitar error 403/500 en Render
CSRF_TRUSTED_ORIGINS = [
    'https://tareadjango.onrender.com',
    'https://*.onrender.com'
]

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# CLOUDINARY CONFIG
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dgk4a9xnk',
    'API_KEY': '644265433378755',
    'API_SECRET': 'htQnHpQ1L0aWa8YvBSM-45ImvCk',
}

cloudinary.config(
    cloud_name = CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key = CLOUDINARY_STORAGE['API_KEY'],
    api_secret = CLOUDINARY_STORAGE['API_SECRET'],
    secure = True
)

# INTERNATIONALIZATION
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STORAGE CONFIG
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage", # Simplificado para evitar errores de manifiesto
    },
}

# CART
CART_SESSION_ID = 'cart'
