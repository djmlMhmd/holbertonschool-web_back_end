#!/usr/bin/env python3
"""Simple function"""


from typing import Iterable, List, Sequence, Tuple

def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """funtion"""
    return [(i, len(i)) for i in lst]
