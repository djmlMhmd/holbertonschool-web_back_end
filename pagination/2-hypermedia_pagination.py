#!/usr/bin/env python3
"""Module for simple pagination"""

import csv
import math
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """Returns a tuple of size two containing a start index and
    an end index corresponding to the range of indexes to return in a list
    for those particular pagination parameters"""

    offset = (page - 1) * page_size
    range = [offset, offset + page_size]
    return tuple(range)


class Server:
    """Server class to paginate database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns a paginated page"""

        """Check that the values' types are correct"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        """Define needed variables"""
        idx_range = index_range(page, page_size)
        start_index = idx_range[0]
        end_index = idx_range[1]
        data = self.dataset()
        the_page = []

        """Check the range"""
        if start_index < len(data) and \
            end_index <= len(data) and \
                start_index <= end_index:
            the_page = data[start_index:end_index]

        return the_page

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Returns dictionary"""

        data = self.get_page(page, page_size)
        total_pages = len(self.dataset()) // page_size
        next_page = None
        prev_page = None

        if page < total_pages:
            next_page = page + 1

        if page > 1:
            prev_page = page - 1

        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
