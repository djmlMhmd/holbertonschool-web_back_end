#!/usr/bin/env python3
""" LIFO Caching
"""

from base_caching import BaseCaching
from collections import deque


class LIFOCache(BaseCaching):
    """LIFOCache class
    """
    def __init__(self):
        """ Constructor class
        """
        super().__init__()
        self.caching_order = deque()

    def put(self, key, item):
        """Insert data into cache
        """
        if key is not None and item is not None:
            if (key not in self.cache_data):
                if len(self.caching_order) + 1 > BaseCaching.MAX_ITEMS:
                    recent_key = self.caching_order.pop()
                    del self.cache_data[recent_key]
                    print(f'DISCARD: {recent_key}')
            self.caching_order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Get the data from cache
        """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
