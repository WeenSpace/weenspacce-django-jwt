import django_jwt
from django_jwt.refresh_token.mixins import RefreshTokenMixin


class Refresh(RefreshTokenMixin, django_jwt.relay.Refresh):
    class Input(RefreshTokenMixin.Fields):
        """Refresh Input"""
