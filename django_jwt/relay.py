from django.contrib.auth import get_user_model

import graphene

from . import mixins
from .decorators import create_token
from .refresh_token.relay import DeleteRefreshTokenCookie, Revoke

__all__ = [
    "JWTMutation",
    "Create",
    "Verify",
    "Refresh",
    "Revoke",
    "DeleteRefreshTokenCookie",
]


class JWTMutation(mixins.CreateJWTMixin, graphene.ClientIDMutation):
    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments["input"]._meta.fields.update(
            {
                get_user_model().USERNAME_FIELD: graphene.InputField(
                    graphene.String,
                    required=True,
                ),
                "password": graphene.InputField(graphene.String, required=True),
            },
        )
        return super().Field(*args, **kwargs)

    @classmethod
    @create_token
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return cls.create(root, info, **kwargs)


class Create(mixins.CreateMixin, JWTMutation):
    """Create JSON Web Token mutation"""


class Verify(mixins.VerifyMixin, graphene.ClientIDMutation):
    class Input:
        token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.verify(*args, **kwargs)


class Refresh(mixins.RefreshMixin, graphene.ClientIDMutation):
    class Input(mixins.RefreshMixin.Fields):
        """Refresh Input"""

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.refresh(*args, **kwargs)


class DeleteJWTCookie(
    mixins.DeleteJWTCookieMixin,
    graphene.ClientIDMutation,
):
    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.delete_cookie(*args, **kwargs)
