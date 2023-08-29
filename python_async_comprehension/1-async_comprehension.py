#!/usr/bin/env python3
"""Module with a asynchronous generator"""

import asyncio
from typing import List

async_generator = __import__("0-async_generator").async_generator

async def async_comprehension() -> List[float]:
    """
    Asynchronous coroutine that collects 10 random numbers using async comprehension.
    """
    return [i async for i in async_generator()]
