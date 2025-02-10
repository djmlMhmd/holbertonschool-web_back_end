#!/usr/bin/env python3
"""Module for encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """A function that hashes the password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """A function that checks if pwd is valid"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
