#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from functools import wraps
import requests
import redis
from typing import Callable

r = redis.Redis()


def cache_results(method: Callable) -> Callable:
    """Decorator to cache the result of a function
    with an expiration time using Redis."""

    @wraps(method)
    def wrapper(url: str) -> str:
        """ A wrapper method"""
        key = 'count:{}'.format(url)

        count = r.get(key)

        if count:
            return count.decode('utf-8')
        else:
            r.incr(key)
            count = r.get(key)
            r.setex(key, 10, count)
            return count.decode('utf-8')

    return wrapper


@cache_results
def get_page(url: str) -> str:
    """Obtain the HTML content
    of a particular URL and returns it."""

    response = requests.get(url)
    return response.text
