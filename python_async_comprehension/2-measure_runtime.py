#!/usr/bin/env python3

import asyncio

async_comprehension = __import__('previous_module_name').async_comprehension

async def measure_runtime():
    """
    Executes async_comprehension four times in parallel and measures the total runtime.
    """

    start_time = asyncio.get_event_loop().time()

    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )

    end_time = asyncio.get_event_loop().time()
    return end_time - start_time

async def main():
    total_runtime = await measure_runtime()
    print("Total runtime:", total_runtime, "seconds")

asyncio.run(main())
