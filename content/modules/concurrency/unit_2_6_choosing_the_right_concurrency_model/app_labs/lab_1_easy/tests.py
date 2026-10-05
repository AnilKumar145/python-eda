"""
Verification Tests for Lab 1 Easy: Hybrid Clinical Gateway
"""

import asyncio
import hashlib
try:
    import solution.solution as starter_code
except (ImportError, ModuleNotFoundError):
    import starter_code
try:
    from solution.solution import compute_genomic_hash, HybridGenomicsGateway
except (ImportError, ModuleNotFoundError):
    from starter_code import compute_genomic_hash, HybridGenomicsGateway


def test_batch_ingest_accuracy():
    gateway = HybridGenomicsGateway(max_workers=2)
    try:
        samples = [
            ("SMP-001", "ATCGATCGATCGAAATTT"),
            ("SMP-002", "GGCCGGCCAATTCCGGAA"),
            ("SMP-003", "TTTTAAAACCCCGGGGAA"),
        ]
        results = asyncio.run(gateway.batch_ingest(samples))
        assert len(results) == 3, f"Expected 3 records, got {len(results)}"

        for item in results:
            sid = item["sample_id"]
            seq = next(s[1] for s in samples if s[0] == sid)
            expected_hash = hashlib.sha256(seq.encode("utf-8")).hexdigest()
            assert item["hash"] == expected_hash, f"Hash mismatch for {sid}"
            assert item["status"] == "PROCESSED"
        print("Test 1 passed! Batch ingestion and multi-process hashing verified.")
    finally:
        gateway.shutdown()


def test_event_loop_responsiveness():
    """Verify that event loop coroutines remain responsive while process pool computes."""
    gateway = HybridGenomicsGateway(max_workers=2)
    try:
        async def _run():
            heavy_sample = ("SMP-HEAVY", "A" * 500_000)
            ping_results = []

            async def quick_ping():
                await asyncio.sleep(0.01)
                ping_results.append("ping_ok")

            # Run heavy process task and quick async task concurrently
            heavy_task = asyncio.create_task(gateway.process_sample(*heavy_sample))
            ping_task = asyncio.create_task(quick_ping())

            await asyncio.gather(heavy_task, ping_task)
            assert "ping_ok" in ping_results
            res = heavy_task.result()
            assert res["status"] == "PROCESSED"

        asyncio.run(_run())
        print("Test 2 passed! Event loop remained responsive during process pool offloading.")
    finally:
        gateway.shutdown()


if __name__ == "__main__":
    test_batch_ingest_accuracy()
    test_event_loop_responsiveness()
    print("All Lab 1 Easy Tests Passed!")
