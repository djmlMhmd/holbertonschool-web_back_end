#!/usr/bin/env python3
"""MRU Cache system"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU Cache class
    """
    def __init__(self):
        """ Constructor method
        """
        super().__init__()
        self.use_order_dict = {}
        self.use_order_num = 0

    def put(self, key, item):
        """Insert data into cache
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                    mru = max(self.use_order_dict.values())
                    for k, _ in self.use_order_dict.items():
                        if self.use_order_dict[k] == mru:
                            del self.cache_data[k]
                            del self.use_order_dict[k]
                            print(f'DISCARD: {k}')
                            break
            self.cache_data[key] = item
            self.use_order_dict[key] = self.use_order_num
            self.use_order_num += 1

    def get(self, key):
        """Get data from cache"""
        if key is not None and key in self.cache_data:
            self.use_order_dict[key] = self.use_order_num
            self.use_order_num += 1
            return self.cache_data[key]
        return None
