"""
Multi-Core Genomic Chromosome Scanner - Solution
"""

import multiprocessing
from typing import Dict, Any


def scan_chromosome_task(chr_id: str, sequence: str, marker: str, out_q: multiprocessing.Queue) -> None:
    count = sequence.count(marker)
    out_q.put((chr_id, count))


class GenomicScannerEngine:
    def scan_all(self, chromosome_dict: Dict[str, str], marker: str) -> Dict[str, int]:
        if not chromosome_dict:
            return {}
            
        out_q = multiprocessing.Queue()
        processes = []
        
        for chr_id, sequence in chromosome_dict.items():
            p = multiprocessing.Process(
                target=scan_chromosome_task,
                args=(chr_id, sequence, marker, out_q),
                name=f"Scanner-{chr_id}"
            )
            processes.append(p)
            p.start()
            
        results: Dict[str, int] = {}
        for _ in chromosome_dict:
            chr_id, count = out_q.get()
            results[chr_id] = count
            
        for p in processes:
            p.join()
            
        return results
