"""
Asynchronous ICU Vital Signs Hub - Starter Code
"""

import asyncio
from typing import List, Dict, Any, Tuple


async def poll_bed(bed_id: str, delay: float, vitals: Dict[str, Any], timeout_sec: float) -> Dict[str, Any]:
    """
    Task 1:
    Simulate polling a single bedside device with delay.
    Enforce timeout_sec using asyncio.wait_for().
    Returns dict with bed_id, status ("OK" or "TIMEOUT"), and vitals.
    """
    # TODO: Implement asynchronous polling with timeout handling
    pass


class AsyncICUVitalHub:
    """
    Task 2:
    Manages concurrent polling of multiple ICU beds on the asyncio event loop.
    """
    @staticmethod
    async def poll_all_beds(
        bed_configs: List[Tuple[str, float, Dict[str, Any]]], 
        timeout_sec: float
    ) -> List[Dict[str, Any]]:
        """
        Poll all bed devices concurrently using asyncio.gather().
        """
        # TODO: Construct coroutine tasks and gather them concurrently
        pass
