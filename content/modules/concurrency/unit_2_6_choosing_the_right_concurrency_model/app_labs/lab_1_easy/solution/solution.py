"""
Hybrid Clinical Gateway - Solution
"""

import asyncio
import hashlib
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Dict, Any


def compute_genomic_hash(sequence: str) -> str:
    return hashlib.sha256(sequence.encode("utf-8")).hexdigest()


class HybridGenomicsGateway:
    def __init__(self, max_workers: int = 2):
        self.pool = ProcessPoolExecutor(max_workers=max_workers)

    async def process_sample(self, sample_id: str, raw_sequence: str) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        digest = await loop.run_in_executor(self.pool, compute_genomic_hash, raw_sequence)
        return {
            "sample_id": sample_id,
            "hash": digest,
            "status": "PROCESSED"
        }

    async def batch_ingest(self, samples: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        tasks = [
            self.process_sample(sample_id, seq)
            for sample_id, seq in samples
        ]
        return await asyncio.gather(*tasks)

    def shutdown(self):
        self.pool.shutdown(wait=True)
