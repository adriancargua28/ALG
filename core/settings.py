"""
Configuración de Django para el portal profesional de Adriana Lara Gutiérrez.

Toda la configuración sensible se lee de variables de entorno (ver README.md).
"""
import os
import urllib.parse
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _env_bool(name, default=False):
    valor = os.environ.get(name)
    if valor is None:
        return default
    return valor.strip().lower() in {"1", "true", "yes", "on", "si", "sí"}


def _env_list(name, default=""):
    return [x.strip() for x in os.environ.get(name, default).split(",") if x.strip()]


# --------------------------------------------------------------------------
# Núcleo
# --------------------------------------------------------------------------
DEBUG = _env_bool("DJANGO_DEBUG", False)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-solo-para-desarrollo-local-no-usar-en-produccion"
    else:
        raise ImproperlyConfigured(
            "Falta la variable de entorno DJANGO_SECRET_KEY. "
            "Para desarrollo local ejecuta antes: DJANGO_DEBUG=1 "
            "(PowerShell: $env:DJANGO_DEBUG='1')."
        )

# En desarrollo Django admite localhost por defecto; en producción hay que
# indicar los dominios: DJANGO_ALLOWED_HOSTS="adrianalara.example,www.adrianalara.example"
ALLOWED_HOSTS = _env_list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = _env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portal.apps.PortalConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# --------------------------------------------------------------------------
# Base de datos
# Con POSTGRES_URL o DATABASE_URL (Vercel + Supabase, Neon...) usa PostgreSQL;
# sin ellas usa SQLite, que basta para trabajar en local.
# --------------------------------------------------------------------------
_db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
if _db_url:
    _u = urllib.parse.urlparse(_db_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _u.path.lstrip("/"),
            "USER": urllib.parse.unquote(_u.username or ""),
            "PASSWORD": urllib.parse.unquote(_u.password or ""),
            "HOST": _u.hostname,
            "PORT": _u.port or 5432,
            "OPTIONS": {"sslmode": "require", "prepare_threshold": None},
            "DISABLE_SERVER_SIDE_CURSORS": True,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("DJANGO_DB_PATH", str(BASE_DIR / "db.sqlite3")),
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------------
# Internacionalización
# --------------------------------------------------------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Archivos estáticos (servidos por WhiteNoise, sin necesidad de Nginx)
# --------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Si falta una entrada del manifiesto de estáticos, se sirve el nombre sin hash
# en lugar de devolver un error 500.
WHITENOISE_MANIFEST_STRICT = False

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}

# --------------------------------------------------------------------------
# Seguridad
# --------------------------------------------------------------------------
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Activar con DJANGO_HTTPS=1 cuando el sitio se sirva con certificado TLS
# (lo habitual tras un proxy inverso o en una plataforma PaaS).
if _env_bool("DJANGO_HTTPS", False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --------------------------------------------------------------------------
# Registro de eventos
# --------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO")},
}