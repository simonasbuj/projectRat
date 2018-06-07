"""
Django settings for projectRat project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7b13r(vc7b)y7sq5@p*)u-$^fm8(+&b8ivz11+w(ild-&f6f0#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', #default django.contrib.sessions
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #3rd party authentication
    'social_django',

    #myapps
    'library',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projectRat.urls'

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
                'social_django.context_processors.backends',  # <- social auth
                'social_django.context_processors.login_redirect', # <- scoial auth
            ],
        },
    },
]

WSGI_APPLICATION = 'projectRat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

#real db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wktlvtji',
        'USER': 'wktlvtji',
        'PASSWORD': 'YUtdlSJELk859rkWDs7hpC0ijMdjysO9',
        'HOST': 'horton.elephantsql.com',
        'PORT': '5432',
    }
}

#mysql db for testing on pythonanywhere
""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'WetPenguin$library',
        'USER': 'WetPenguin',
        'PASSWORD': 'LOKYS123',
        'HOST': 'WetPenguin.mysql.pythonanywhere-services.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
    }
} """


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
#where to collect files use pythona manage.py collectstatic in console
#STATIC_ROOT ='../static'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/') #where {%collect static%} collects files

MEDIA_URL = '/uploaded_files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploaded_files')


#additional dirs to look for static files
#its not even working
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/main"),    
]

#login logout
#LOGOUT_REDIRECT_URL = os.path.join(BASE_DIR, 'knygos')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'social_core.backends.facebook.FacebookOAuth2', # for Facebook authentication ;d

    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'accounts:login'
LOGIN_ERROR_URL = 'accounts:login'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '201422127269-o6kt77vsnjdadhbn0labpt63vo2npblm.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'SAJZ3FqIppoSdPx9HX-Ufleu'

SOCIAL_AUTH_FACEBOOK_KEY = '889491574575981'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'c03b68b5bd242f6b0201f56f4b0656d3'  # App Secret


#when going live this is important for Facebook login :d;d;
# Force https redirect
#SECURE_SSL_REDIRECT = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Force HTTPS in the final URIs
#SOCIAL_AUTH_REDIRECT_IS_HTTPS = True