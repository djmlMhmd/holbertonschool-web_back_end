#!/usr/bin/env python3
"""Simple function"""


from typing import List, Tuple

def element_length(lst: List[str]) -> List[Tuple[str, int]]:
    """funtion"""
    return [(i, len(i)) for i in lst]
