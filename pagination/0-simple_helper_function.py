#!/usr/bin/env python3
"""Module with simple helper function"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """Returns tuple of size two containin start index and
    an end index corresponding to the range of indexes to return in a list
    for those particular pagination parameters"""

    offset = (page - 1) * page_size
    range = [offset, offset + page_size]
    return tuple(range)
