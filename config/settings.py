from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────
# SECURITY & BASIC
# ─────────────────────────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this-in-production")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,0.0.0.0"
).split(",")

# Railway tự động cung cấp domain qua biến này
RAILWAY_HOST = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
if RAILWAY_HOST:
    ALLOWED_HOSTS.append(RAILWAY_HOST)

# ─────────────────────────────────────────────────────────
# APPS
# ─────────────────────────────────────────────────────────

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

# ─────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # phải ngay sau SecurityMiddleware
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

# ─────────────────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────────────────

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

# ─────────────────────────────────────────────────────────
# DATABASE (Railway PostgreSQL hoặc local SQLite fallback)
# ─────────────────────────────────────────────────────────

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# Local fallback: nếu không có DATABASE_URL hoặc đang DEBUG → dùng SQLite
if "DATABASE_URL" not in os.environ or DEBUG:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

# ─────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────────────────

LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────────────────
# STATIC FILES (Whitenoise cho production)
# ─────────────────────────────────────────────────────────

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ─────────────────────────────────────────────────────────
# MEDIA
# ─────────────────────────────────────────────────────────

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─────────────────────────────────────────────────────────
# SITE & ALLAUTH (cập nhật config mới, loại bỏ deprecated)
# ─────────────────────────────────────────────────────────

SITE_ID = 1

LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Cấu hình allauth mới (thay thế các setting deprecated)
ACCOUNT_LOGIN_METHODS = {"email": True}  # đăng nhập bằng email
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"  # hoặc "mandatory"
ACCOUNT_UNIQUE_EMAIL = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    },
    "facebook": {
        "APP": {
            "client_id": os.getenv("FACEBOOK_APP_ID", ""),
            "secret": os.getenv("FACEBOOK_APP_SECRET", ""),
            "key": "",
        },
        "METHOD": "oauth2",
        "SCOPE": ["email", "public_profile"],
    },
}

# ─────────────────────────────────────────────────────────
# CELERY
# ─────────────────────────────────────────────────────────

REDIS_URL = os.getenv("REDIS_URL", "")

# BUG FIX: Nếu REDIS_URL rỗng → set None, tránh Celery crash khi không có Redis
CELERY_BROKER_URL = REDIS_URL or None
CELERY_RESULT_BACKEND = REDIS_URL or None

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"

# ─────────────────────────────────────────────────────────
# SECURITY (Production)
# ─────────────────────────────────────────────────────────

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # BUG FIX: Không override ALLOWED_HOSTS = ["*"] ở đây
    # Railway domain đã được append ở trên qua RAILWAY_PUBLIC_DOMAIN
    # Nếu muốn cho phép mọi host (không khuyến khích): uncomment dòng dưới
    # ALLOWED_HOSTS = ["*"]