"""
Django settings for recoco project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from multisite import SiteID

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
    "multisite",
    "reversion",
    "reversion_compare",
    "django.contrib.admin",
    "hijack",
    "hijack.contrib.admin",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "guardian",
    "magicauth",
    "sass_processor",
    "django_vite",
    "markdownx",
    "dbtemplates",
    "tagging",
    "taggit",
    "modelcluster",
    "leaflet",
    "django_gravatar",
    "actstream",
    "notifications",
    "rest_framework",
    "rest_framework_simplejwt",
    "generic_relations",
    "django_filters",
    "csvexport",
    "captcha",
    "ordered_model",
    "dynamic_forms",
    "watson",
    "phonenumber_field",
    "cookie_consent",
    "recoco.apps.dsrc",
    "recoco.apps.onboarding",
    "recoco.apps.home",
    "recoco.apps.projects",
    "recoco.apps.tasks",
    "recoco.apps.resources",
    "recoco.apps.geomatics",
    "recoco.apps.addressbook",
    "recoco.apps.survey",
    "recoco.apps.reminders",
    "recoco.apps.communication",
    "recoco.apps.invites",
    "recoco.apps.crm",
    "recoco.apps.training",
    "recoco.apps.pages",
    "recoco.apps.metrics",
    "recoco.apps.demarches_simplifiees",
    "crispy_forms",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "django_celery_results",
]

SITE_ID = SiteID(default=1)

SILENCED_SYSTEM_CHECKS = [
    "sites.E101"  # Check to ensure SITE_ID is an int - ours is an object
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "multisite.middleware.DynamicSiteMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "sesame.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "watson.middleware.SearchContextMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "recoco.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "recoco.apps.projects.context_processors.is_switchtender_processor",
                "recoco.apps.projects.context_processors.active_project_processor",
                "recoco.apps.projects.context_processors.unread_notifications_processor",
            ],
            "loaders": [
                "dbtemplates.loader.Loader",
                "multisite.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "libraries": {
                "common_tags": "recoco.templatetags.common_extra",
                "dsrc_tags": "recoco.apps.dsrc.templatetags.dsrc_tags",
            },
        },
    },
]

# DB Templates
DBTEMPLATES_USE_CODEMIRROR = True

# MULTISITE
MULTISITE_DEFAULT_TEMPLATE_DIR = "default_site/"

CRISPY_ALLOWED_TEMPLATE_PACKS = ["dsrc_crispy_forms", "dsrc_crispy_forms_no_js"]
CRISPY_TEMPLATE_PACK = "dsrc_crispy_forms"

WSGI_APPLICATION = "recoco.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
    "sesame.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# GUARDIAN
GUARDIAN_USER_OBJ_PERMS_MODEL = "home.UserObjectPermissionOnSite"
GUARDIAN_GROUP_OBJ_PERMS_MODEL = "home.GroupObjectPermissionOnSite"

# SESAME Configuration
SESAME_MAX_AGE = 60 * 60 * 24 * 10
SESAME_ONE_TIME = False

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
    "compressor.finders.CompressorFinder",
]

# UPLOAD

MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")
MEDIA_URL = "media/"

SASS_PRECISION = 8

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, "recoco/static/css"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Configuration
EMAIL_FROM = "Recoco <no-reply@recoco.fr>"

# MagicAuth configuration
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "login-redirect"
MAGICAUTH_FROM_EMAIL = EMAIL_FROM
MAGICAUTH_ADAPTER = "recoco.apps.home.adapters.UVMagicauthAdapter"
MAGICAUTH_EMAIL_SUBJECT = "Connectez-vous à Recoco ici"
MAGICAUTH_EMAIL_FIELD = "email"
MAGICAUTH_LOGGED_IN_REDIRECT_URL_NAME = "login-redirect"
MAGICAUTH_TOKEN_DURATION_SECONDS = 60 * 60 * 24 * 3

# MARKDOWNX
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown_link_attr_modifier",
    "sane_lists",  # https://python-markdown.github.io/extensions/sane_lists/
]

MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    "markdown_link_attr_modifier": {
        "new_tab": "on",
        "no_referrer": "external_only",
        "auto_title": "on",
    },
}

# Tagging
FORCE_LOWERCASE_TAGS = True
TAGGIT_CASE_INSENSITIVE = True

# Session Settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 30 * 24 * 60 * 60  # 30d * 24h * 60m * 60s

##Cookie consent settings
COOKIE_CONSENT_HTTPONLY = False

# emails to use for notifications
TEAM_EMAILS = ["friches@beta.gouv.fr"]

# BREVO
BREVO_API_KEY = "NO-API-KEY-DEFINED"


# IFrames
X_FRAME_OPTIONS = "SAMEORIGIN"

# RECAPTCHA, V3
RECAPTCHA_REQUIRED_SCORE = 0.85

# DYNAMIC FORMS
DYNAMIC_FORMS_CUSTOM_JS = ""

# ALLAUTH
ACCOUNT_ADAPTER = "recoco.apps.home.adapters.UVAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 20
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/login-redirect"

ACCOUNT_FORMS = {
    "login": "recoco.apps.home.forms.UVLoginForm",
    "signup": "recoco.apps.home.forms.UVSignupForm",
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "reset_password": "recoco.apps.home.forms.UVResetPasswordForm",
    "reset_password_from_key": "recoco.apps.home.forms.UVResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
}

# Django vite
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "frontend/dist"
STATICFILES_DIRS += [DJANGO_VITE_ASSETS_PATH]


# Phonenumbers
PHONENUMBER_DEFAULT_REGION = "FR"

# Hijack
HIJACK_PERMISSION_CHECK = "hijack.permissions.superusers_and_staff"

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_xml.renderers.XMLRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8) if DEBUG else timedelta(minutes=5),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "TOKEN_OBTAIN_SERIALIZER": "recoco.rest_api.serializers.CustomTokenObtainPairSerializer",
}

# WAGTAIL
WAGTAIL_SITE_NAME = "Recommandations Collaboratives"
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
WAGTAIL_EMAIL_MANAGEMENT_ENABLED = False

# WAGTAILADMIN_BASE_URL = define that

# Materialized views
MATERIALIZED_VIEWS_SPEC = [
    {
        "name": "projects",
        "unique_indexes": ["hash"],
        "indexes": ["created_on"],
    },
    {
        "name": "recommendations",
        "unique_indexes": ["hash"],
        "indexes": ["created_on"],
    },
    {
        "name": "resources",
        "unique_indexes": ["hash"],
    },
    {
        "name": "users",
        "unique_indexes": ["hash"],
        "indexes": ["last_login", "is_advisor"],
    },
]

MATERIALIZED_VIEWS_SQL_DIR = BASE_DIR / "apps/metrics/sql_queries"

# Baker
# https://model-bakery.readthedocs.io/en/latest/how_bakery_behaves.html#customizing-baker
BAKER_CUSTOM_CLASS = "recoco.tests.CustomBaker"

# CELERY
CELERY_TIMEZONE = "Europe/Paris"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = "django-db"


# Metabase
METABASE_HOST = os.environ.get("METABASE_HOST")
METABASE_API_KEY = os.environ.get("METABASE_API_KEY")


# Démarches simplifiées
DS_BASE_URL = "https://www.demarches-simplifiees.fr/"
DS_API_BASE_URL = f"{DS_BASE_URL}api/public/v1/"

# eof
