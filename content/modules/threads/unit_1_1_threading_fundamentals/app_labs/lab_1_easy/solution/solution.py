"""
Bedside Monitor Telemetry Ingestion - Solution
"""

import threading
import time
from typing import List, Tuple, Dict, Any


def read_sensor(device_id: str, latency: float, value: Any, output_dict: Dict[str, Any]) -> None:
    time.sleep(latency)
    output_dict[device_id] = {
        "device_id": device_id,
        "value": value,
        "timestamp": time.time()
    }


class TelemetryIngestionEngine:
    def poll_monitors(self, monitor_configs: List[Tuple[str, float, Any]]) -> Dict[str, Any]:
        output_dict: Dict[str, Any] = {}
        threads: List[threading.Thread] = []
        
        for device_id, latency, value in monitor_configs:
            t = threading.Thread(
                target=read_sensor,
                args=(device_id, latency, value, output_dict),
                name=f"Poller-{device_id}"
            )
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        return output_dict
