#!/usr/bin/env python3
""" FIFO Caching"""

from base_caching import BaseCaching
from collections import deque


class FIFOCache(BaseCaching):
    """A FIFO Caching class
    """
    def __init__(self):
        """ The contstructor method
        """
        super().__init__()
        self.insertion_order = deque()

    def put(self, key, item):
        """ Insert a data into cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.insertion_order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            oldest_key = self.insertion_order.popleft()
            del self.cache_data[oldest_key]
            print(f"DISCARD: {oldest_key}")

    def get(self, key):
        """ Get data from cache
        """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
