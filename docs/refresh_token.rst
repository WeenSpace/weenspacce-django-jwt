Refresh token
=============

This package supports two refresh methods:

* `Single token refresh <#single-token-refresh>`__ (by default)
* `Long running refresh tokens <#long-running-refresh-tokens>`__

Single token refresh
--------------------

Settings
~~~~~~~~

::

    DJANGO_JWT = {
        "JWT_VERIFY_EXPIRATION": True,
        "JWT_EXPIRATION_DELTA": timedelta(minutes=5),
        "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    }

It means that you need to refresh every 5 mins (``payload.exp``) and even you keep on refreshing token every 5 mins, you will still be logout in 7 days after the first token has been issued (``refreshExpiresIn``).

Queries
~~~~~~~

* ``refreshToken`` to obtain a brand new *token* with renewed expiration time for **non-expired tokens**:

::

    mutation RefreshToken($token: String!) {
      refreshToken(token: $token) {
        token
        payload
        refreshExpiresIn
      }
    }

**Refresh and keeping tokens alive**

.. figure:: https://user-images.githubusercontent.com/5514990/34951332-e67845f0-fa3b-11e7-8e72-09d610e73025.png
   :alt: before

**Refresh after 4 minutes...**

.. figure:: https://user-images.githubusercontent.com/5514990/34951331-e2ff9680-fa3b-11e7-8f0a-dbb3845367a7.png
   :alt: after

1. Token issued

  ::

    exp = orig_iat + JWT_EXPIRATION_DELTA (payload.exp)
    refreshToken (t): exp = t + JWT_EXPIRATION_DELTA

2. Signature expiration (login is required)

  ::

    when: t = exp
    exp = refresh_at + JWT_EXPIRATION_DELTA
    verifyToken (t): error! if JWT_VERIFY_EXPIRATION=true

3. Refresh expiration

  ::

    when: t = orig_iat + JWT_REFRESH_EXPIRATION_DELTA (refreshExpiresIn)
    refreshToken (t): error!

Long running refresh tokens
---------------------------

Refresh tokens stored on database.

Add ``django_jwt.refresh_token`` to your *INSTALLED\_APPS*::

    INSTALLED_APPS = [
        ...
        "django_jwt.refresh_token.apps.RefreshTokenConfig",
        ...
    ]

Settings
~~~~~~~~

::

    DJANGO_JWT = {
        "JWT_VERIFY_EXPIRATION": True,
        "JWT_REFRESH_TOKEN_LONG_RUNNING": True,
        "JWT_EXPIRATION_DELTA": timedelta(minutes=5),
        "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    }

It means that you need to refresh every 5 mins (``payload.exp``) and you need to replace your refresh token in 7 days after it has been issued (``refreshExpiresIn``).

Schema
~~~~~~

Add mutations to the root schema::

    import graphene
    import django_jwt


    class Mutation(graphene.ObjectType):
        create_token = django_jwt.Create.Field()
        verify_token = django_jwt.Verify.Field()
        refresh_token = django_jwt.Refresh.Field()
        revoke_token = django_jwt.Revoke.Field()

    schema = graphene.Schema(mutation=Mutation)

Queries
~~~~~~~

* ``tokenAuth`` to authenticate the user and obtain a **JSON Web Token** and **Refresh Token**:

  ::

      mutation TokenAuth($username: String!, $password: String!) {
        tokenAuth(username: $username, password: $password) {
          token
          payload
          refreshToken
          refreshExpiresIn
        }
      }


* ``refreshToken`` to refresh your *token*, using the ``refreshToken`` you already got during authorization:

  ::

      mutation RefreshToken($refreshToken: String!) {
        refreshToken(refreshToken: $refreshToken) {
          token
          payload
          refreshToken
          refreshExpiresIn
        }
      }


* ``revokeToken`` to revoke a valid ``refreshToken``. The invalidation takes place immediately, and the ``refreshToken`` cannot be used again after the revocation:

  ::

      mutation RevokeToken($refreshToken: String!) {
        revokeToken(refreshToken: $refreshToken) {
          revoked
        }
      }


Per-cookie
~~~~~~~~~~

When a refresh token is requested and ``jwt_cookie`` decorator is set, the response will set the given cookie with the refresh token string.

Unlimited refresh
~~~~~~~~~~~~~~~~~

Configure the ``JWT_REFRESH_EXPIRED_HANDLER`` setting that checks if the refresh token is expired::

    DJANGO_JWT = {
        "JWT_VERIFY_EXPIRATION": True,
        "JWT_REFRESH_TOKEN_LONG_RUNNING": True,
        "JWT_REFRESH_EXPIRED_HANDLER": lambda orig_iat, context: False,
    }

One time only use refresh token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatically revoke a refresh token after it has been used::

    from django.dispatch import receiver

    from django_jwt.refresh_token.signals import refresh_token_rotated


    @receiver(refresh_token_rotated)
    def revoke_refresh_token(sender, request, refresh_token, **kwargs):
        refresh_token.revoke(request)

Clear refresh tokens
~~~~~~~~~~~~~~~~~~~~

  .. automethod:: django_jwt.refresh_token.management.commands.cleartokens.Command.handle

Delete revoked refresh tokens with ``cleartokens`` command.

.. code:: sh

    $ python manage.py cleartokens --help

    usage: cleartokens [--expired]

    optional arguments:
      --expired             Clears expired tokens

The ``--expired`` argument allows the user to remove those refresh tokens whose lifetime is greater than the amount specified by ``JWT_REFRESH_EXPIRATION_DELTA`` setting.
