#!/usr/bin/env python3
"""Module containing a function to create and return an asyncio task."""

import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Creates an asyncio task for wait_random."""
    task = asyncio.create_task(wait_random(max_delay))
    return task
