#!/usr/bin/env python3
"""Module containing functions to measure
execution time of async operations."""

import asyncio
import time

# Importing the wait_random and wait_n functions from external modules
wait_random = __import__('0-basic_async_syntax').wait_random
wait_n = __import__("1-concurrent_coroutines").wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the average execution time for wait_n.

    Returns:
        float: Average execution time per wait_n call.
    """

    async def async_measure():
        """
        An asynchronous function to measure execution time.

        Returns:
            float: Average execution time per wait_n call.
        """
        start = time.time()
        await wait_n(n, max_delay)
        end = time.time()
        return (end - start) / n

    return asyncio.run(async_measure())
