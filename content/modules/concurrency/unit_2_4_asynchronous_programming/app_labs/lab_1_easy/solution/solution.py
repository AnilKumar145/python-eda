"""
Asynchronous ICU Vital Signs Hub - Solution
"""

import asyncio
from typing import List, Dict, Any, Tuple


async def _simulate_fetch(delay: float, vitals: Dict[str, Any]) -> Dict[str, Any]:
    await asyncio.sleep(delay)
    return vitals


async def poll_bed(bed_id: str, delay: float, vitals: Dict[str, Any], timeout_sec: float) -> Dict[str, Any]:
    try:
        data = await asyncio.wait_for(_simulate_fetch(delay, vitals), timeout=timeout_sec)
        return {
            "bed_id": bed_id,
            "status": "OK",
            "vitals": data
        }
    except asyncio.TimeoutError:
        return {
            "bed_id": bed_id,
            "status": "TIMEOUT",
            "vitals": {}
        }


class AsyncICUVitalHub:
    @staticmethod
    async def poll_all_beds(
        bed_configs: List[Tuple[str, float, Dict[str, Any]]], 
        timeout_sec: float
    ) -> List[Dict[str, Any]]:
        tasks = [
            poll_bed(bed_id, delay, vitals, timeout_sec)
            for bed_id, delay, vitals in bed_configs
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
