"""
Bedside Monitor Telemetry Ingestion - Starter Code
"""

import threading
import time
from typing import List, Tuple, Dict, Any


def read_sensor(device_id: str, latency: float, value: Any, output_dict: Dict[str, Any]) -> None:
    """
    Simulate reading telemetry from an individual bedside device over TCP.
    
    Args:
        device_id: Unique hardware identifier
        latency: Simulated network latency in seconds
        value: Clinical measurement value
        output_dict: Shared dictionary storing output
    """
    # ========================================================================
    # WRITE CODE HERE (Task 1)
    # ========================================================================
    pass
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


class TelemetryIngestionEngine:
    """Gateway engine coordinating concurrent device telemetry reads."""
    
    def poll_monitors(self, monitor_configs: List[Tuple[str, float, Any]]) -> Dict[str, Any]:
        """
        Poll all configured bedside monitors concurrently.
        
        Args:
            monitor_configs: List of (device_id, latency, value) tuples.
            
        Returns:
            Dictionary mapping device_id to telemetry record.
        """
        # ========================================================================
        # WRITE CODE HERE (Task 2)
        # ========================================================================
        pass
        # ========================================================================
        # END OF YOUR CODE
        # ========================================================================
