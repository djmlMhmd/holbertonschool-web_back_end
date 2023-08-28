#!/usr/bin/env python3
"""Simple function"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """function returning a function"""
    def the_multiplier(n: float) -> float:
        """multiplier function"""
        return n * multiplier
    return the_multiplier
