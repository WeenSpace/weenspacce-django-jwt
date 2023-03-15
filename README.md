<p align="center">
  <a href="https://github.com/WeenSpace/weenspace-django-jwt/"><img width="420px" src="https://github.com/WeenSpace/weenspace-django-jwt/_static/logo.png" alt='Django GraphQL JWT'></a>
</p>

<p align="center">
    JSON Web Token authentication for Django GraphQL.
    <br>Fantastic <strong>documentation</strong> is available at <a href="https://github.com/WeenSpace/weenspace-django-jwt">https://github.com/WeenSpace/weenspace-django-jwt</a>.
</p>
<p align="center">
    <a href="https://github.com/WeenSpace/weenspace-django-jwt/actions">
        <img src="https://github.com/WeenSpace/weenspace-django-jwt/actions/workflows/test-suite.yml/badge.svg" alt="Test">
    </a>
    <a href="https://codecov.io/gh/flavors/weenspace-django-jwt">
        <img src="https://img.shields.io/codecov/c/github/flavors/weenspace-django-jwt?color=%2334D058" alt="Coverage">
    </a>
    <a href="https://www.codacy.com/gh/flavors/weenspace-django-jwt/dashboard">
        <img src="https://app.codacy.com/project/badge/Grade/4f9fd439fbc74be88a215b9ed2abfcf9" alt="Codacy">
    </a>
    <a href="https://pypi.python.org/pypi/weenspace-django-jwt">
        <img src="https://img.shields.io/pypi/v/weenspace-django-jwt.svg" alt="Package version">
    </a>
</p>

## Installation

Install last stable version from Pypi:

```sh
pip install weenspace-django-jwt
```

Add `AuthenticationMiddleware` middleware to your *MIDDLEWARE* settings:


```py
MIDDLEWARE = [
    # ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # ...
]
```

Add `JWTMiddleware` middleware to your *GRAPHENE* settings:

```py
GRAPHENE = {
    "SCHEMA": "mysite.myschema.schema",
    "MIDDLEWARE": [
        "django_jwt.middleware.JWTMiddleware",
    ],
}
```

Add `JWTBackend` backend to your *AUTHENTICATION_BACKENDS*:

```py
AUTHENTICATION_BACKENDS = [
    "django_jwt.backends.JWTBackend",
    "django.contrib.auth.backends.ModelBackend",
]
```

## Schema

Add *weenspace-django-jwt* mutations to the root schema:

```py
import graphene
import django_jwt


class Mutation(graphene.ObjectType):
    create_token = django_jwt.Create.Field()
    verify_token = django_jwt.Verify.Field()
    refresh_token = django_jwt.Refresh.Field()


schema = graphene.Schema(mutation=Mutation)
```
