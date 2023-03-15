from django_jwt.backends import JWTBackend
from django_jwt.exceptions import JWTError
from django_jwt.settings import jwt_settings

from .testcases import TestCase


class BackendsTests(TestCase):
    def setUp(self):
        super().setUp()
        self.backend = JWTBackend()

    def test_authenticate(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {self.token}"
            ),
        }

        request = self.request_factory.get("/", **headers)
        user = self.backend.authenticate(request=request)

        self.assertEqual(user, self.user)

    def test_authenticate_fail(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} invalid"
            ),
        }

        request = self.request_factory.get("/", **headers)

        with self.assertRaises(JWTError):
            self.backend.authenticate(request=request)

    def test_authenticate_null_request(self):
        user = self.backend.authenticate(request=None)
        self.assertIsNone(user)

    def test_authenticate_missing_token(self):
        request = self.request_factory.get("/")
        user = self.backend.authenticate(request=request)

        self.assertIsNone(user)

    def test_get_user(self):
        user = self.backend.get_user(self.user.pk)
        self.assertEqual(user, self.user)
