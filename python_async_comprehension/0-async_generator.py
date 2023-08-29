#!/usr/bin/env python3

import asyncio
import random

async def async_generator():
    """
    Asynchronous coroutine that generates random numbers.
    """

    for _ in range(10):
        await asyncio.sleep(1)  # Asynchronously wait for 1 second
        yield random.randint(0, 10)  # Yield a random number between 0 and 10

# Example usage
async def main():
    async for number in async_generator():
        print("Generated:", number)

asyncio.run(main())
