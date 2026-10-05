"""
Multi-Core Genomic Chromosome Scanner - Starter Code
"""

import multiprocessing
import time
from typing import Dict, Any


def scan_chromosome_task(chr_id: str, sequence: str, marker: str, out_q: multiprocessing.Queue) -> None:
    """
    Top-level worker function scanning for target marker in sequence.
    """
    # ========================================================================
    # WRITE CODE HERE (Task 1)
    # ========================================================================
    pass
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


class GenomicScannerEngine:
    """Multi-process engine coordinating parallel DNA sequence alignment."""
    
    def scan_all(self, chromosome_dict: Dict[str, str], marker: str) -> Dict[str, int]:
        """
        Scan all chromosomes in parallel across independent OS processes.
        """
        # ========================================================================
        # WRITE CODE HERE (Task 2)
        # ========================================================================
        pass
        # ========================================================================
        # END OF YOUR CODE
        # ========================================================================
