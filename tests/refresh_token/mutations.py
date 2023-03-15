import django_jwt
from django_jwt.refresh_token.mixins import RefreshTokenMixin


class Refresh(RefreshTokenMixin, django_jwt.Refresh):
    class Arguments(RefreshTokenMixin.Fields):
        """Refresh Arguments"""
