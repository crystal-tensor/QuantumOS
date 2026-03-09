import sys
import os

# Ensure the SDK is in the python path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from spectrum_os.core import quantum_task

# --- User Code ---

@quantum_task(required_qubits=2, expected_time_ns=5000, tenant_id="user_alice_001", priority=10)
def prepare_bell_state(theta: float):
    """
    This is a sample quantum program that prepares a Bell state.
    """
    # In a real scenario, this would generate QISA instructions
    # q = QuantumRegister(2)
    # H(q[0])
    # CX(q[0], q[1])
    # RZ(theta, q[0])
    pass

if __name__ == "__main__":
    print("--- Simulating Quantum Task Submission ---\n")
    
    # Call the decorated function
    # This will trigger the interception, JSON generation, and HTTP submission
    response = prepare_bell_state(theta=1.57)
    
    if response:
        print("\nJob Submission Result:")
        print(response)
    else:
        print("\nJob Submission finished (with possible connection warning).")
    
    print("\n--- End of Simulation ---")
