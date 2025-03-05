#!/usr/bin/env python3
"""
A module with a class to manage API authentication
"""

from flask import request
from os import getenv
from typing import List, TypeVar


class Auth():
    """
    A class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A public method that checks if path requieres authorization"""
        if (path is None or
                excluded_paths is None or
                excluded_paths == []):
            return True

        if not path.endswith('/'):
            path = path + '/'

        if path in excluded_paths:
            return False

        for e_path in excluded_paths:
            if e_path.endswith("*") and path.startswith(e_path[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """A public method fo authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request:
        """
        authorization_header = self.authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        decoded_b64_auth_header = self.decode_base64_authorization_header(
            base64_authorization_header)
        user_credentials = self.extract_user_credentials(
            decoded_b64_auth_header)

        user = self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
        if user is None:
            return None
        return user

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(getenv("SESSION_NAME"))
