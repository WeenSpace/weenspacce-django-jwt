import graphene

import django_jwt

from . import mixins
from .testcases import CookieTestCase, SchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):
    query = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        create_token = django_jwt.Create.Field()


class VerifyTests(mixins.VerifyMixin, SchemaTestCase):
    query = """
    mutation VerifyToken($token: String!) {
      verifyToken(token: $token) {
        payload
      }
    }"""

    class Mutation(graphene.ObjectType):
        verify_token = django_jwt.Verify.Field()


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):
    query = """
    mutation RefreshToken($token: String) {
      refreshToken(token: $token) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = django_jwt.Refresh.Field()


class CookieTokenAuthTests(mixins.CookieTokenAuthMixin, CookieTestCase):
    query = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        create_token = django_jwt.Create.Field()


class CookieRefreshTests(mixins.CookieRefreshMixin, CookieTestCase):
    query = """
    mutation {
      refreshToken {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = django_jwt.Refresh.Field()


class DeleteCookieTests(mixins.DeleteCookieMixin, CookieTestCase):
    query = """
    mutation {
      deleteCookie {
        deleted
      }
    }"""

    class Mutation(graphene.ObjectType):
        delete_cookie = django_jwt.DeleteJWTCookie.Field()
