#!/usr/bin/env python3
"""Exercice module to learn to work with Redis"""

from functools import wraps
import redis
from typing import Callable, Optional, Union
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Counts how many times methods of the
    Cache class are called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """The wrapper for decorator"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and
    outputs for a particular function
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """The wrapper for decorator"""
        input_values = str(args)
        self._redis.rpush(input_key, input_values)
        output_values = str(method(self, *args, **kwargs))
        self._redis.rpush(output_key, output_values)
        return output_values

    return wrapper


def replay(function: Callable):
    """
    Ouputs the history of calls of a particular function
    with inputs and outputs
    """
    r = redis.Redis()
    function_name = function.__qualname__
    nb_of_calls = r.get(function_name)

    try:
        nb_of_calls = nb_of_calls.decode('utf-8')
    except Exception:
        nb_of_calls = 0
    print(f'{function_name} was called {nb_of_calls} times:')

    inputs = r.lrange(function_name + ":inputs", 0, -1)
    outputs = r.lrange(function_name + ":outputs", 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""
        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        print('{}(*{}) -> {}'.format(function_name, input, output))


class Cache():
    """The cache class"""

    def __init__(self) -> None:
        """The constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """A method to store the data"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Reading from redis and reconering original key
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)

        return value

    def get_str(self, key: str) -> str:
        """From redis bytes to string"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: int) -> int:
        """
        From redis bytes to integer
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
