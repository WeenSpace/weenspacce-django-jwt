INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django_jwt.refresh_token.apps.RefreshTokenConfig",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    },
}

SECRET_KEY = "test"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django_jwt.backends.JWTBackend",
]

GRAPHENE = {
    "MIDDLEWARE": ["django_jwt.middleware.JWTMiddleware"],
}
