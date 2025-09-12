"""Proactive callback loop using asyncio."""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, List


class ProactiveLoop:
    """Run callbacks on a schedule in the background."""

    def __init__(self, callbacks: List[Callable[[], Awaitable[None]]], interval: float = 1800) -> None:
        """Initialize the loop.

        Args:
            callbacks: Functions to run periodically.
            interval: Number of seconds between runs. Defaults to 30 minutes.
        """
        self.callbacks = callbacks
        self.interval = interval
        self.paused = False

    def pause(self) -> None:
        """Pause executing callbacks."""
        self.paused = True

    def resume(self) -> None:
        """Resume executing callbacks."""
        self.paused = False

    async def run(self) -> None:
        """Run callbacks every ``interval`` seconds."""
        while True:
            if not self.paused:
                for callback in self.callbacks:
                    await callback()
            await asyncio.sleep(self.interval)


async def hydration_reminder() -> None:
    """Example callback reminding the user to drink water."""
    print("Hydration reminder: drink some water!")


def start_proactive_loop(callbacks: List[Callable[[], Awaitable[None]]]) -> ProactiveLoop:
    """Start a :class:`ProactiveLoop` in the current event loop."""
    loop = ProactiveLoop(callbacks)
    asyncio.get_running_loop().create_task(loop.run())
    return loop
