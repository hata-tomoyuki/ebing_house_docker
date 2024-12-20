"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()
IS_DOCKER = os.getenv('IS_DOCKER', False)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IS_DOCKER = os.path.exists('/.dockerenv')
IS_HEROKU = os.getenv('DYNO') is not None

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = os.getenv('DEBUG')=='True'

ALLOWED_HOSTS = [os.getenv('HEROKU_APP_COM'),'127.0.0.1', 'localhost',
                 '172.25.139.129']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'wlist.apps.WlistConfig',
    ##追加
    'rest_framework',
    'rest_framework.authtoken',
    'api_user.apps.ApiUserConfig',
    'api_word.apps.ApiWordConfig',
    'api_memo1.apps.ApiMemo1Config',
    'api_memo2.apps.ApiMemo2Config',
    ## 追加1201
    'corsheaders',
]


# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = '/accounts/login/'


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'


# MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

MIDDLEWARE = [
    #  ## 追加1201
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',

]

# MIDDLEWARE += ["corsheaders.middleware.CorsMiddleware"]

## 追加1201
# CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',  # ReactアプリのURL
#     'https://front-rho-red.vercel.app',  # 本番のReactアプリURL
# ]

# CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOW_HEADERS = [
#     "content-type",
#     "authorization",
#     'X-CSRFToken',
# ]

# CORS_ALLOW_METHODS = [
#     'DELETE',
#     'GET',
#     'POST',
#     'PUT',
#     'PATCH',
#     'OPTIONS',
# ]

# CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOW_HEADERS = [
#     "content-type",
#     "authorization",
#     'X-CSRFToken',
# ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR,'templates'],
        'DIRS': [BASE_DIR / 'static/react',
                 BASE_DIR / 'templates'],  # React の index.html を指す

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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # MySQLを使用する
        'NAME': os.getenv('DB_NAME'),          # 作成したデータベース名
        'USER': os.getenv('DB_USER'),          # 作成したユーザー名
        'PASSWORD': os.getenv('DB_PASSWORD'),  # 作成したユーザーのパスワード
        'HOST': 'db',
        'PORT': '3306',                        # MySQLのデフォルトポート
    }
}



# Herokuの環境変数からDATABASE_URLが提供されている場合、その設定を使用
# DATABASE_URL = os.getenv('DATABASE_URL')
# if DATABASE_URL:
#     DATABASES = {
#         'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
#     }

# Herokuの環境変数からJAWSDB_URLが提供されている場合、その設定を使用
DATABASE_URL = os.getenv('JAWSDB_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
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

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # 本番環境で必要。ファイルを1場所にまとめるため。

STATICFILES_DIRS = [
    str(BASE_DIR / 'static'),  # 現在の静的ファイル
    str(BASE_DIR / 'build/static'),  # Reactのビルド成果物
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_TRUSTED_ORIGINS = ['https://'+ os.getenv('HEROKU_APP_COM'),
                        'http://localhost:3000',  # ReactアプリのURL
                        'https://front-rho-red.vercel.app',
                        ]

##################'
# Email settings #
##################

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


##################
# Authentication #
##################

AUTH_USER_MODEL = 'accounts.CustomUser'


##################
# Logging        #
##################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

##################
# Caches         #
##################

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

##################
# Media          #
##################

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
ALLOW_MEDIA_DELIVERY_IN_PRODUCTION = True

