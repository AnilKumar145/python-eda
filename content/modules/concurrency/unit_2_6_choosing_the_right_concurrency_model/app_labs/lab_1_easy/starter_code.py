"""
Hybrid Clinical Gateway - Starter Code
"""

import asyncio
import hashlib
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Dict, Any


def compute_genomic_hash(sequence: str) -> str:
    """
    Task 1:
    Top-level CPU worker function.
    Computes SHA-256 hash of the sequence string.
    """
    # TODO: Implement SHA-256 hash computation
    pass


class HybridGenomicsGateway:
    """
    Task 2 & 3:
    Hybrid async ingestion gateway offloading CPU hashing to a ProcessPoolExecutor.
    """
    def __init__(self, max_workers: int = 2):
        # TODO: Initialize process pool
        self.pool = None

    async def process_sample(self, sample_id: str, raw_sequence: str) -> Dict[str, Any]:
        """
        Offload compute_genomic_hash to self.pool via loop.run_in_executor().
        """
        # TODO: Asynchronously offload to process pool
        pass

    async def batch_ingest(self, samples: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """
        Ingest batch of samples concurrently on the asyncio event loop.
        """
        # TODO: Gather sample tasks concurrently
        pass

    def shutdown(self):
        """Cleanly shutdown the worker process pool."""
        # TODO: Shutdown pool
        pass
