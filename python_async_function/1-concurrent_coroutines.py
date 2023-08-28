#!/usr/bin/env python3
"""function with integers n and max_delay as
arguments that measures the total execution"""

import asyncio
import random
from typing import List


async def wait_random(max_delay: int = 10) -> float:
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay

async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous routine that spawns wait_random n times with specified max_delay.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): The maximum delay in seconds for wait_random.

    Returns:
        List[float]: List of delays in ascending order.
    """
    tasks = [wait_random(max_delay) for _ in range(n)]

    delays = await asyncio.gather(*tasks)

    return sorted(delays)
