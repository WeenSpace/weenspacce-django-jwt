import graphene

import django_jwt

from ..testcases import SchemaTestCase
from . import mixins
from .mutations import Refresh
from .testcases import CookieTestCase


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):
    query = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshToken
        refreshExpiresIn
      }
    }"""

    refresh_token_mutations = {
        "create_token": django_jwt.Create,
    }


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):
    query = """
    mutation RefreshToken($refreshToken: String) {
      refreshToken(refreshToken: $refreshToken) {
        token
        payload
        refreshToken
        refreshExpiresIn
      }
    }"""

    refresh_token_mutations = {
        "refresh_token": Refresh,
    }


class RevokeTests(mixins.RevokeMixin, SchemaTestCase):
    query = """
    mutation RevokeToken($refreshToken: String!) {
      revokeToken(refreshToken: $refreshToken) {
        revoked
      }
    }"""

    class Mutation(graphene.ObjectType):
        revoke_token = django_jwt.Revoke.Field()


class CookieTokenAuthTests(mixins.CookieTokenAuthMixin, CookieTestCase):
    query = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshToken
        refreshExpiresIn
      }
    }"""

    refresh_token_mutations = {
        "create_token": django_jwt.Create,
    }


class CookieRefreshTests(mixins.CookieRefreshMixin, CookieTestCase):
    query = """
    mutation {
      refreshToken {
        token
        payload
        refreshToken
        refreshExpiresIn
      }
    }"""

    refresh_token_mutations = {
        "refresh_token": Refresh,
    }


class DeleteCookieTests(mixins.DeleteCookieMixin, CookieTestCase):
    query = """
    mutation {
      deleteCookie {
        deleted
      }
    }"""

    class Mutation(graphene.ObjectType):
        delete_cookie = django_jwt.DeleteRefreshTokenCookie.Field()
