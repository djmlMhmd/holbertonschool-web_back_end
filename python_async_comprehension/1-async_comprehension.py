#!/usr/bin/env python3

import asyncio

async_generator = __import__('previous_module_name').async_generator

async def async_comprehension():
    """
    Asynchronous coroutine that collects 10 random numbers using async comprehension.
    """

    random_numbers = [number async for number in async_generator()]
    return random_numbers

async def main():
    numbers = await async_comprehension()
    print("Collected random numbers:", numbers)

asyncio.run(main())
