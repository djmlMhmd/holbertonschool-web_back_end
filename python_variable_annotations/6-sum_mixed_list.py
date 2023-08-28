#!/usr/bin/env python3
"""Simple function"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """sum function"""
    return float(sum(mxd_lst))
