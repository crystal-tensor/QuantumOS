import numpy as np
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
import math
import sys
import os

# Ensure q_sim is in path
sys.path.append(os.path.dirname(__file__))

# Mock VirtualQubit for standalone running if file missing
try:
    from virtual_backend import VirtualQubit
except ImportError:
    class VirtualQubit:
        def __init__(self, t1_us, t2_us, frequency_ghz):
            self.t1_us = t1_us
            self.t2_us = t2_us
            self.frequency_ghz = frequency_ghz

app = FastAPI()

class QisaInstruction(BaseModel):
    opcode: str
    operands: List[Any] = []
    target_qubits: Optional[List[int]] = None

class QuantumSimulator:
    def __init__(self, n_qubits: int):
        self.n_qubits = n_qubits
        self.dim = 2 ** n_qubits
        self.rho = np.zeros((self.dim, self.dim), dtype=complex)
        self.rho[0, 0] = 1.0
        self.qubits = [VirtualQubit(t1_us=50.0, t2_us=70.0, frequency_ghz=5.0) for _ in range(n_qubits)]

    def apply_gate(self, gate_matrix: np.ndarray, target_qubits: List[int]):
        # Use expansion for all gates to be consistent and support arbitrary targets
        U = self._expand_gate(gate_matrix, target_qubits)
        self.rho = U @ self.rho @ U.conj().T

    def _expand_gate(self, gate_matrix: np.ndarray, target_qubits: List[int]) -> np.ndarray:
        U = np.zeros((self.dim, self.dim), dtype=complex)
        num_targets = len(target_qubits)
        
        for k in range(self.dim):
            # Decompose basis state k into bits
            bits = [(k >> (self.n_qubits - 1 - i)) & 1 for i in range(self.n_qubits)]
            
            # Extract target bits
            current_target_val = 0
            for i, q_idx in enumerate(target_qubits):
                current_target_val |= bits[q_idx] << (num_targets - 1 - i)
                
            # Get the column from gate matrix corresponding to this basis state component
            # The gate maps |current_target_val> -> sum(coeff * |out_val>)
            col = gate_matrix[:, current_target_val]
            
            for out_val, coeff in enumerate(col):
                if abs(coeff) < 1e-12: continue
                
                # Construct output state bits
                out_bits = list(bits)
                for i, q_idx in enumerate(target_qubits):
                    out_bits[q_idx] = (out_val >> (num_targets - 1 - i)) & 1
                    
                # Reconstruct full index
                out_k = 0
                for bit in out_bits:
                    out_k = (out_k << 1) | bit
                    
                U[out_k, k] += coeff
        return U

    def apply_idle_noise(self, duration_ns: int):
        t_us = duration_ns / 1000.0
        for i in range(self.n_qubits):
            q = self.qubits[i]
            gamma_1 = 1.0 - np.exp(-t_us / q.t1_us) if q.t1_us > 0 else 0.0
            
            K0_t1 = np.array([[1, 0], [0, np.sqrt(1 - gamma_1)]], dtype=complex)
            K1_t1 = np.array([[0, np.sqrt(gamma_1)], [0, 0]], dtype=complex)
            
            target_coherence_decay = np.exp(-t_us / q.t2_us) if q.t2_us > 0 else 0.0
            amp_damping_coherence_decay = np.sqrt(1 - gamma_1)
            
            if amp_damping_coherence_decay > 0:
                extra_decay = target_coherence_decay / amp_damping_coherence_decay
            else:
                extra_decay = 0.0
            if extra_decay > 1.0: extra_decay = 1.0
            
            p_phase = (1.0 - extra_decay) / 2.0
            K0_phase = np.sqrt(1 - p_phase) * np.eye(2, dtype=complex)
            K1_phase = np.sqrt(p_phase) * np.array([[1, 0], [0, -1]], dtype=complex)
            
            self._apply_kraus_to_qubit(i, [K0_t1, K1_t1])
            self._apply_kraus_to_qubit(i, [K0_phase, K1_phase])

    def _apply_kraus_to_qubit(self, qubit_idx: int, kraus_ops: List[np.ndarray]):
        new_rho = np.zeros_like(self.rho)
        for K in kraus_ops:
            K_full = self._expand_gate(K, [qubit_idx])
            new_rho += K_full @ self.rho @ K_full.conj().T
        self.rho = new_rho

    def measure(self, shots: int) -> Dict[str, int]:
        probs = np.real(np.diag(self.rho))
        if np.sum(probs) == 0: probs[:] = 1.0 / len(probs) # Fallback
        probs = probs / np.sum(probs)
        
        counts = {}
        rng = np.random.default_rng()
        samples = rng.choice(len(probs), size=shots, p=probs)
        
        for s in samples:
            bin_str = format(s, f'0{self.n_qubits}b')
            counts[bin_str] = counts.get(bin_str, 0) + 1
        return counts

@app.post("/driver/run")
async def run_simulation(instructions: List[QisaInstruction]):
    try:
        max_q = 0
        for instr in instructions:
            if instr.target_qubits:
                for q in instr.target_qubits:
                    max_q = max(max_q, q)
        
        n_qubits = max_q + 1
        sim = QuantumSimulator(n_qubits)
        
        for instr in instructions:
            if instr.opcode == "WAIT":
                duration = int(instr.operands[0])
                sim.apply_idle_noise(duration)
            elif instr.opcode == "H":
                H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
                sim.apply_gate(H, instr.target_qubits or [0])
            elif instr.opcode == "X":
                X = np.array([[0, 1], [1, 0]], dtype=complex)
                sim.apply_gate(X, instr.target_qubits or [0])
            elif instr.opcode == "Y":
                Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
                sim.apply_gate(Y, instr.target_qubits or [0])
            elif instr.opcode == "Z":
                Z = np.array([[1, 0], [0, -1]], dtype=complex)
                sim.apply_gate(Z, instr.target_qubits or [0])
            elif instr.opcode == "CX" or instr.opcode == "CNOT":
                CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
                sim.apply_gate(CX, instr.target_qubits)
            elif instr.opcode == "RX":
                theta = float(instr.operands[0])
                RX = np.array([[np.cos(theta/2), -1j*np.sin(theta/2)], [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)
                sim.apply_gate(RX, instr.target_qubits or [0])
            elif instr.opcode == "RY":
                theta = float(instr.operands[0])
                RY = np.array([[np.cos(theta/2), -np.sin(theta/2)], [np.sin(theta/2), np.cos(theta/2)]], dtype=complex)
                sim.apply_gate(RY, instr.target_qubits or [0])
            elif instr.opcode == "RZ":
                theta = float(instr.operands[0])
                RZ = np.array([[np.exp(-1j*theta/2), 0], [0, np.exp(1j*theta/2)]], dtype=complex)
                sim.apply_gate(RZ, instr.target_qubits or [0])
                
        return sim.measure(shots=1000)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
