
from pathlib import Path
import os

from datetime import timedelta
from rest_framework.settings import api_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = ''


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)(1o_79=i=bscn+v2nx7%lcr%9!q^_xv$3=#up&5@-*3a0y4og"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "admin_interface",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "bookstore",
    "colorfield",
    "corsheaders",
    "knox",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "bookstoreapi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'build')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookstoreapi.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#CORS

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    # ],
     'DEFAULT_AUTHENTICATION_CLASSES':('knox.auth.TokenAuthentication',),
}

#------------------------------- KNOX SETTINGS -------------------------------

REST_KNOX = {
    'SECURE_HASH_ALGORITHM':'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64, 
    'TOKEN_TTL': timedelta(minutes=45), 
    'USER_SERIALIZER': 'knox.serializers.UserSerializer',
    'TOKEN_LIMIT_PER_USER': None,
    'AUTO_REFRESH': False, 
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}


# AUTH_USER_MODEL = 'bookstore.Client'




#----------------------------   JAZZMIN SETTINGS -----------------------------

JAZZMIN_SETTINGS = {
    "site_title": "Bookstore",
    "site_brand": "Bookstore Admin Panel",
    #"site_logo": "images/logo-bookstore2.png",
    "login_logo": None,
    "welcome_sign": "Welcome to the Bookstore Admin Interface",
    "copyright": "Bookstore",

    "search_model": ["auth.User"],

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,


    
      # Links to put along the top menu
    "topmenu_links": [
         
         # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

         # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

         # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "bookstore"},
    ],

   


    "usermenu_links": [
        {"model": "auth.user"}
    ],

    "order_with_respect_to": ["bookstore", "auth" ],



    "hide_apps": ["admin_interface"],
    "changeform_format": "horizontal_tabs",
    
   
     "language_chooser": True,

     
    }

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": True,
    "brand_colour": "navbar-secondary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True,
    
}

# Have a lot of themes to use !
# JAZZMIN_SETTINGS["show_ui_builder"] = True
