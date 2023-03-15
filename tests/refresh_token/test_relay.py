import graphene

import django_jwt

from ..testcases import RelaySchemaTestCase
from . import mixins
from .relay import Refresh
from .testcases import RelayCookieTestCase


class TokenAuthTests(mixins.TokenAuthMixin, RelaySchemaTestCase):
    query = """
    mutation TokenAuth($input: ObtainJWTInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
        clientMutationId
      }
    }"""

    refresh_token_mutations = {
        "create_token": django_jwt.relay.Create,
    }


class RefreshTokenTests(mixins.RefreshMixin, RelaySchemaTestCase):
    query = """
    mutation RefreshToken($input: RefreshInput!) {
      refreshToken(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
        clientMutationId
      }
    }"""

    refresh_token_mutations = {
        "refresh_token": Refresh,
    }


class RevokeTokenTests(mixins.RevokeMixin, RelaySchemaTestCase):
    query = """
    mutation RevokeToken($input: RevokeInput!) {
      revokeToken(input: $input) {
        revoked
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        revoke_token = django_jwt.relay.Revoke.Field()


class CookieTokenAuthTests(mixins.CookieTokenAuthMixin, RelayCookieTestCase):
    query = """
    mutation TokenAuth($input: ObtainJWTInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
        clientMutationId
      }
    }"""

    refresh_token_mutations = {
        "create_token": django_jwt.relay.Create,
    }


class CookieRefreshTests(mixins.CookieRefreshMixin, RelayCookieTestCase):
    query = """
    mutation {
      refreshToken(input: {}) {
        token
        payload
        refreshToken
        refreshExpiresIn
      }
    }"""

    refresh_token_mutations = {
        "refresh_token": Refresh,
    }


class DeleteCookieTests(mixins.DeleteCookieMixin, RelayCookieTestCase):
    query = """
    mutation {
      deleteCookie(input: {}) {
        deleted
      }
    }"""

    class Mutation(graphene.ObjectType):
        delete_cookie = django_jwt.relay.DeleteRefreshTokenCookie.Field()
