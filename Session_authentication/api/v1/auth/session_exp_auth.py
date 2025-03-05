#!/usr/bin/env python3
"""A module for exp session auth"""


from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """A class for session Auth"""

    def __init__(self):
        """The class constructor method"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ A session creation method with expiration"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id, "created_at": datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns user_id based on session ID"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]["user_id"]

        if "created_at" not in self.user_id_by_session_id[session_id]:
            return None

        created_at = self.user_id_by_session_id[session_id]["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return self.user_id_by_session_id[session_id]["user_id"]
