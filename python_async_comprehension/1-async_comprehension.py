#!/usr/bin/env python3

import asyncio
from typing import List

async_generator = __import__('previous_module_name').async_generator

async def async_comprehension() -> List[float]:
    """
    Asynchronous coroutine that collects 10 random numbers using async comprehension.
    """
    return [i async for i in async_generator()]
