from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,0.0.0.0,.ngrok-free.dev"
    ).split(",")
]

# CSRF cho ngrok
CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.dev",
]

# Fix OAuth HTTPS khi dùng ngrok
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# Railway domain
RAILWAY_HOST = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
if RAILWAY_HOST:
    ALLOWED_HOSTS.append(RAILWAY_HOST)

# ─────────────────────────────────────────
# APPS
# ─────────────────────────────────────────

INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "core.apps.CoreConfig",

    "django_htmx",
    "crispy_forms",
    "crispy_bootstrap5",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",

]

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ─────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

# ─────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],

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

WSGI_APPLICATION = "config.wsgi.application"

# ─────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# fallback SQLite khi local
if "DATABASE_URL" not in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─────────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────────

AUTHENTICATION_BACKENDS = [

    "django.contrib.auth.backends.ModelBackend",

    "allauth.account.auth_backends.AuthenticationBackend",

]

ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]

# ─────────────────────────────────────────
# SOCIAL LOGIN
# ─────────────────────────────────────────

SOCIALACCOUNT_PROVIDERS = {

    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online"
        },
    },

    "facebook": {

        "METHOD": "oauth2",

        "SCOPE": [
            "email",
            "public_profile",
        ],

        "AUTH_PARAMS": {
            "auth_type": "reauthenticate"
        },
    }
}

# ─────────────────────────────────────────
# PASSWORD
# ─────────────────────────────────────────

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

# ─────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# ─────────────────────────────────────────
# STATIC
# ─────────────────────────────────────────

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ─────────────────────────────────────────
# DEFAULT PK
# ─────────────────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"