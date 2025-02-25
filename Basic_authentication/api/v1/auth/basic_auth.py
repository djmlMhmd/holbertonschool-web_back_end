#!/usr/bin/env python3
"""
Basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Basic auth class to manage the API authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        function to extract the base64 encoded authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        encoded = authorization_header.split(" ", 1)[1]

        return encoded

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        function to decode the base64 encoded authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded = base64_authorization_header.encode("utf-8")
            decoded64 = base64.b64decode(encoded)
            decoded = decoded64.decode("utf-8")
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        function to extract the username and password
        from the base64 encoded authorization header
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(":", 1)

        return credentials[0], credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        function to extract the user object from the database
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            find_user = User.search({'email': user_email})
        except BaseException:
            return None

        for user in find_user:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        function to extract the current user from the request
        """
        auth_header = self.authorization_header(request)

        if not auth_header:
            return None

        encoded = self.extract_base64_authorization_header(auth_header)

        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)

        if not decoded:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded)

        if not user_email or not user_pwd:
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
