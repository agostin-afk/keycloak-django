import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-demo-keycloak-nao-use-em-producao",
)
DEBUG = os.environ.get("DEBUG", "1") == "1"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "demo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Keycloak
KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL", "http://keycloak:8080")
KEYCLOAK_PUBLIC_URL = os.environ.get("KEYCLOAK_PUBLIC_URL", "http://localhost:8080")
REALM = os.environ.get("OIDC_OP_REALM", "demo")

OIDC_RP_CLIENT_ID = os.environ.get("OIDC_RP_CLIENT_ID", "django-app")
OIDC_RP_CLIENT_SECRET = os.environ.get(
    "OIDC_RP_CLIENT_SECRET", "django-secret-change-me"
)

OIDC_OP_AUTHORIZATION_ENDPOINT = (
    f"{KEYCLOAK_PUBLIC_URL}/realms/{REALM}/protocol/openid-connect/auth"
)
OIDC_OP_TOKEN_ENDPOINT = (
    f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
)
OIDC_OP_USER_ENDPOINT = (
    f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo"
)
OIDC_OP_LOGOUT_ENDPOINT = (
    f"{KEYCLOAK_PUBLIC_URL}/realms/{REALM}/protocol/openid-connect/logout"
)

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/protegido/"
LOGOUT_REDIRECT_URL = "/"
