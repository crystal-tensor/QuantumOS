import numpy as np
import cmath

class VirtualQubit:
    def __init__(self, t1_us: float, t2_us: float, frequency_ghz: float):
        """
        Initialize a Virtual Qubit with physical parameters.
        
        Args:
            t1_us: Relaxation time in microseconds.
            t2_us: Dephasing time in microseconds.
            frequency_ghz: Resonance frequency in GHz.
        """
        self.t1_us = t1_us
        self.t2_us = t2_us
        self.frequency_ghz = frequency_ghz
        
        # Initialize density matrix to |0><0|
        # State is represented as a 2x2 density matrix to support mixed states (noise)
        self.rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)

    def apply_idle_noise(self, duration_ns: int):
        """
        Apply T1 and T2 relaxation/dephasing noise to the qubit state.
        
        The evolution of the density matrix under relaxation (T1) and dephasing (T2)
        can be described by the operator-sum representation (Kraus operators) or
        directly modifying the density matrix elements.
        
        For a single qubit:
        rho_00(t) = 1 + (rho_00(0) - 1) * exp(-t/T1)
        rho_11(t) = rho_11(0) * exp(-t/T1)
        rho_01(t) = rho_01(0) * exp(-t/T2)
        rho_10(t) = rho_10(0) * exp(-t/T2)
        
        Args:
            duration_ns: Idle duration in nanoseconds.
        """
        if duration_ns <= 0:
            return

        t_us = duration_ns / 1000.0
        
        # Calculate decay factors
        # Prevent division by zero if T1 or T2 are 0 (though physically impossible for functional qubits)
        exp_t1 = np.exp(-t_us / self.t1_us) if self.t1_us > 0 else 0.0
        exp_t2 = np.exp(-t_us / self.t2_us) if self.t2_us > 0 else 0.0
        
        # Update diagonal elements (Population relaxation - T1)
        # rho_11 decays to 0, rho_00 grows to 1
        rho_11_old = self.rho[1, 1]
        self.rho[1, 1] = rho_11_old * exp_t1
        self.rho[0, 0] = 1.0 - self.rho[1, 1] # Trace preservation
        
        # Update off-diagonal elements (Coherence relaxation - T2)
        self.rho[0, 1] *= exp_t2
        self.rho[1, 0] *= exp_t2


    def set_state(self, alpha: complex, beta: complex):
        """
        Set the qubit to a pure state |psi> = alpha|0> + beta|1>.
        Using density matrix representation rho = |psi><psi|.
        """
        # Ensure alpha and beta are complex numbers
        alpha = complex(alpha)
        beta = complex(beta)
        
        norm = abs(alpha)**2 + abs(beta)**2
        if not np.isclose(norm, 1.0) and norm > 0:
             # Normalize if needed
             alpha /= np.sqrt(norm)
             beta /= np.sqrt(norm)
             
        psi = np.array([alpha, beta])
        self.rho = np.outer(psi, np.conj(psi))

    def get_fidelity(self, target_alpha: complex, target_beta: complex) -> float:
        """
        Calculate the fidelity of the current state with respect to a target pure state.
        F(rho, |psi>) = <psi|rho|psi>
        """
        target_psi = np.array([target_alpha, target_beta])
        # F = <psi | rho | psi>
        # rho | psi>
        temp = np.dot(self.rho, target_psi)
        # <psi | temp
        fidelity = np.dot(np.conj(target_psi), temp)
        return float(np.real(fidelity))

    def measure_prob_0(self) -> float:
        """Return probability of measuring 0 (population of ground state)."""
        return float(np.real(self.rho[0, 0]))

