#!/usr/bin/env python3
"""Simple function"""

from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """function return tuple"""
    return (k, float(v * v))
