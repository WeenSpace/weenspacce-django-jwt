Quickstart
==========

Dependencies
------------

* Python ≥ 3.6
* Django ≥ 2.0


Installation
------------

Install last stable version v\ |version| from Pypi::

    pip install weenspace-django-jwt

Add ``AuthenticationMiddleware`` middleware to your *MIDDLEWARE* settings:

.. code:: python

    MIDDLEWARE = [
        ...
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        ...
    ]

Add ``JWTMiddleware`` middleware to your *GRAPHENE* settings::

    GRAPHENE = {
        "SCHEMA": "mysite.myschema.schema",
        "MIDDLEWARE": [
            "django_jwt.middleware.JWTMiddleware",
        ],
    }

Add ``JWTBackend`` backend to your *AUTHENTICATION_BACKENDS*::

    AUTHENTICATION_BACKENDS = [
        "django_jwt.backends.JWTBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]


Schema
------

Add mutations to the root schema::

    import graphene
    import django_jwt


    class Mutation(graphene.ObjectType):
        create_token = django_jwt.Create.Field()
        verify_token = django_jwt.Verify.Field()
        refresh_token = django_jwt.Refresh.Field()


    schema = graphene.Schema(mutation=Mutation)


Queries
-------

* ``tokenAuth`` to authenticate the user and obtain a **JSON Web Token**.

  The mutation uses your User's model `USERNAME_FIELD <https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#django.contrib.auth.models.CustomUser>`_, which by default is ``username``:

  ::

      mutation TokenAuth($username: String!, $password: String!) {
        tokenAuth(username: $username, password: $password) {
          token
          payload
          refreshExpiresIn
        }
      }


* ``verifyToken`` to validate the *token* and obtain the *token payload*:

  ::

      mutation VerifyToken($token: String!) {
        verifyToken(token: $token) {
          payload
        }
      }


* ``refreshToken`` to obtain a brand new *token* with renewed expiration time:

  :doc:`Configure your refresh token <refresh_token>` scenario and set to ``True`` the :doc:`JWT_VERIFY_EXPIRATION<settings>` setting.
