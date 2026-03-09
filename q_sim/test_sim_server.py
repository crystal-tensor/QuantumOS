import httpx
import time
import subprocess
import sys
import os
import signal
import json

def test_simulation():
    url = "http://localhost:8001/driver/run"
    
    # Define a Bell state circuit with some noise
    # H(0) -> CX(0, 1) -> WAIT(0, 50000) -> MEASURE
    # Note: sim_server logic for WAIT applies to all qubits in the current implementation
    # "sim.apply_idle_noise(duration)" applies to all.
    
    payload = [
        {"opcode": "QALLOC", "operands": [2]},
        {"opcode": "H", "target_qubits": [0]},
        {"opcode": "CX", "target_qubits": [0, 1]},
        # Wait 10us (10000ns). T1=50us. exp(-10/50) = exp(-0.2) ~= 0.818
        # Signal should decay towards |00>.
        # Bell state is (|00> + |11>).
        # |11> decays to |10> then |00>. |00> stays |00>.
        # So we expect more 00 than 11.
        {"opcode": "WAIT", "operands": [10000]}, 
        {"opcode": "MEASURE", "target_qubits": [0, 1]}
    ]
    
    print(f"Sending payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = httpx.post(url, json=payload, timeout=10.0)
        response.raise_for_status()
        result = response.json()
        print("Simulation Result:", result)
        
        # specific check
        total_shots = sum(result.values())
        print(f"Total shots: {total_shots}")
        
        if "00" in result and "11" in result:
            print("Bell state correlations observed.")
        else:
            print("Warning: Missing expected states 00 or 11.")
            
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)

def main():
    # Start the server
    print("Starting sim_server...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "sim_server:app", "--host", "0.0.0.0", "--port", "8001"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        test_simulation()
    finally:
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()
        # Print server output if any error
        stdout, stderr = server_process.communicate()
        if server_process.returncode != 0 and server_process.returncode != -15: # -15 is SIGTERM
            print("Server Output:\n", stdout.decode())
            print("Server Error:\n", stderr.decode())

if __name__ == "__main__":
    main()
