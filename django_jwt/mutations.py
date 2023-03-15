from django.contrib.auth import get_user_model

import graphene

from . import mixins
from .decorators import create_token
from .refresh_token.mutations import DeleteRefreshTokenCookie, Revoke

__all__ = [
    "JWTMutation",
    "Create",
    "Verify",
    "Refresh",
    "Revoke",
    "DeleteRefreshTokenCookie",
]


class JWTMutation(mixins.CreateJWTMixin, graphene.Mutation):
    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update(
            {
                get_user_model().USERNAME_FIELD: graphene.String(required=True),
                "password": graphene.String(required=True),
            },
        )
        return super().Field(*args, **kwargs)

    @classmethod
    @create_token
    def mutate(cls, root, info, **kwargs):
        return cls.create(root, info, **kwargs)


class Create(mixins.CreateMixin, JWTMutation):
    """Obtain JSON Web Token mutation"""


class Verify(mixins.VerifyMixin, graphene.Mutation):
    class Arguments:
        token = graphene.String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        return cls.verify(*args, **kwargs)


class Refresh(mixins.RefreshMixin, graphene.Mutation):
    class Arguments(mixins.RefreshMixin.Fields):
        """Refresh Arguments"""

    @classmethod
    def mutate(cls, *arg, **kwargs):
        return cls.refresh(*arg, **kwargs)


class DeleteJWTCookie(mixins.DeleteJWTCookieMixin, graphene.Mutation):
    @classmethod
    def mutate(cls, *args, **kwargs):
        return cls.delete_cookie(*args, **kwargs)
