import graphene

import django_jwt

from . import mixins
from .testcases import RelayCookieTestCase, RelaySchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, RelaySchemaTestCase):
    query = """
    mutation TokenAuth($input: ObtainJWTInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshExpiresIn
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        create_token = django_jwt.relay.Create.Field()


class VerifyTests(mixins.VerifyMixin, RelaySchemaTestCase):
    query = """
    mutation VerifyToken($input: VerifyInput!) {
      verifyToken(input: $input) {
        payload
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        verify_token = django_jwt.relay.Verify.Field()


class RefreshTests(mixins.RefreshMixin, RelaySchemaTestCase):
    query = """
    mutation RefreshToken($input: RefreshInput!) {
      refreshToken(input: $input) {
        token
        payload
        refreshExpiresIn
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = django_jwt.relay.Refresh.Field()


class CookieTokenAuthTests(mixins.CookieTokenAuthMixin, RelayCookieTestCase):
    query = """
    mutation TokenAuth($input: ObtainJWTInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshExpiresIn
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        create_token = django_jwt.relay.Create.Field()


class CookieRefreshTests(mixins.CookieRefreshMixin, RelayCookieTestCase):
    query = """
    mutation {
      refreshToken(input: {}) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = django_jwt.relay.Refresh.Field()


class DeleteCookieTests(mixins.DeleteCookieMixin, RelayCookieTestCase):
    query = """
    mutation {
      deleteCookie(input: {}) {
        deleted
      }
    }"""

    class Mutation(graphene.ObjectType):
        delete_cookie = django_jwt.relay.DeleteJWTCookie.Field()
