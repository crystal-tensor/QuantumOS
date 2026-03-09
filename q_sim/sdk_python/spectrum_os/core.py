import json
import uuid
import inspect
import functools
import time
import httpx
from typing import Callable, Any, Dict, List, Optional

class QuantumTaskError(Exception):
    pass

def quantum_task(required_qubits: int, expected_time_ns: int, tenant_id: str = "default", priority: int = 0):
    """
    Decorator to intercept a Python function and package it as a QuantumOS Job.
    
    Args:
        required_qubits: Number of qubits required for this task.
        expected_time_ns: Estimated execution time in nanoseconds.
        tenant_id: Identifier for the user or organization submitting the job.
        priority: Job priority (higher value = higher priority).
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a unique Job ID
            job_id = str(uuid.uuid4())
            
            # Capture function source code (future: parse AST to QISA)
            try:
                source_code = inspect.getsource(func)
            except OSError:
                source_code = "Source not available"

            # Capture arguments
            func_args = {
                "args": args,
                "kwargs": kwargs
            }

            # Construct the standardized JSON Payload
            # This must match the api_contract_v1.json JobRequest schema
            payload = {
                "job_id": job_id,
                "tenant_id": tenant_id,
                "required_qubits": required_qubits,
                "expected_duration_ns": expected_time_ns,
                "priority": priority,
                # For now, generate a dummy instruction since we don't have a compiler yet
                "qisa_instructions": [
                    {
                        "opcode": "WAIT",
                        "operands": [100],
                        "target_qubits": []
                    }
                ]
            }
            
            # Serialize to JSON string for logging/debugging
            json_payload = json.dumps(payload, indent=2)
            print(f"[SDK] Generated Payload:\n{json_payload}")

            # Send the job to the Rust Kernel
            kernel_url = "http://127.0.0.1:3000/api/v1/submit_job"
            max_retries = 3
            timeout_seconds = 5.0
            
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"[SDK] Sending job to {kernel_url} (Attempt {attempt}/{max_retries})...")
                    with httpx.Client(timeout=timeout_seconds) as client:
                        response = client.post(kernel_url, json=payload)
                        response.raise_for_status()
                        print(f"[SDK] Job submitted successfully. Response: {response.json()}")
                        return response.json()
                except httpx.ConnectError:
                    print(f"[SDK] Connection failed. Is the kernel running?")
                    if attempt == max_retries:
                        print("[SDK] Max retries reached. Giving up.")
                        # Gracefully handle connection error as per requirements
                        print("请求已发出，等待内核响应 (Simulation: Connection failed)")
                        # Verify logic: if connection fails, we might want to return the payload or None
                        # The requirement says "catch ConnectionError and print gracefully".
                        return None
                    time.sleep(1) # Wait before retry
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 503:
                        print(f"[SDK] Service Unavailable (503). Is the kernel running?")
                        if attempt == max_retries:
                            print("[SDK] Max retries reached. Giving up.")
                            print("请求已发出，等待内核响应 (Simulation: Connection failed/Service Unavailable)")
                            return None
                        time.sleep(1)
                        continue
                    
                    print(f"[SDK] HTTP Error: {e.response.status_code} - {e.response.text}")
                    raise QuantumTaskError(f"Job submission failed: {e}")
                except Exception as e:
                    print(f"[SDK] Unexpected error: {e}")
                    raise QuantumTaskError(f"Job submission failed: {e}")
            
            return None
            
        return wrapper
    return decorator
