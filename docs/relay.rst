Relay
=====

Complete support for `Relay <https://facebook.github.io/relay/>`_.

Schema
------

Add mutations to the root schema::

    import graphene
    import django_jwt


    class Mutation(graphene.ObjectType):
        create_token = django_jwt.relay.Create.Field()
        verify_token = django_jwt.relay.Verify.Field()
        refresh_token = django_jwt.relay.Refresh.Field()
        delete_token_cookie = django_jwt.relay.DeleteJWTCookie.Field()

        # Long running refresh tokens
        revoke_token = django_jwt.relay.Revoke.Field()

        delete_refresh_token_cookie = \
            django_jwt.relay.DeleteRefreshTokenCookie.Field()


    schema = graphene.Schema(mutation=Mutation)


Queries
-------

Relay mutations only accepts one argument named *input*.


* ``tokenAuth`` to authenticate the user and obtain a **JSON Web Token**:

  ::

      mutation TokenAuth($username: String!, $password: String!) {
        tokenAuth(input: {username: $username, password: $password}) {
          token
          payload
          refreshExpiresIn
        }
      }

* ``verifyToken`` to validate the *token* and obtain the *token payload*:

  ::

      mutation VerifyToken($token: String!) {
        verifyToken(input: {token: $token}) {
          payload
        }
      }


Single token refresh
~~~~~~~~~~~~~~~~~~~~

* ``refreshToken`` to obtain a brand new *token* with renewed expiration time for **non-expired tokens**:

  ::

      mutation RefreshToken($token: String!) {
        refreshToken(input: {token: $token}) {
          token
          payload
          refreshExpiresIn
        }
      }


Long running refresh tokens
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``refreshToken`` to refresh your *token*, using the ``refreshToken`` you already got during authorization:

  ::

      mutation RefreshToken($refreshToken: String!) {
        refreshToken(input: {refreshToken: $refreshToken}) {
          token
          payload
          refreshToken
          refreshExpiresIn
        }
      }

* ``revokeToken`` to revoke a valid ``refreshToken``. The invalidation takes place immediately, and the ``refreshToken`` cannot be used again after the revocation:

  ::

      mutation RevokeToken($refreshToken: String!) {
        revokeToken(input: {refreshToken: $refreshToken}) {
          revoked
        }
      }


Cookies
~~~~~~~

* ``deleteTokenCookie`` to delete the ``JWT`` cookie:

  ::

      mutation {
        deleteTokenCookie(input: {}) {
          deleted
        }
      }

* ``deleteRefreshTokenCookie`` to delete ``JWT-refresh-token`` cookie for :doc:`long running refresh tokens<refresh_token>`.

  ::

      mutation {
        deleteRefreshTokenCookie(input: {}) {
          deleted
        }
      }


Customizing
-----------

If you want to customize the ``Create`` behavior, you'll need to customize the ``resolve()`` method on a subclass of:

  .. autoclass:: django_jwt.relay.JWTMutation

::

    import graphene
    import django_jwt


    class Create(django_jwt.relay.JWTMutation):
        user = graphene.Field(UserType)

        @classmethod
        def resolve(cls, root, info, **kwargs):
            return cls(user=info.context.user)

Authenticate the user and obtain a **JSON Web Token** and the *user id*::

    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(input: {username: $username, password: $password}) {
        token
        payload
        refreshExpiresIn
        user {
          id
        }
      }
    }
