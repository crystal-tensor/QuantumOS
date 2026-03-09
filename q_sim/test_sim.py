import pytest
import numpy as np
from virtual_backend import VirtualQubit

def test_initialization():
    # Test initialization with reasonable parameters
    qubit = VirtualQubit(t1_us=50.0, t2_us=70.0, frequency_ghz=5.0)
    
    # Expect ground state |0><0|
    # [[1, 0], [0, 0]]
    expected_rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    np.testing.assert_array_almost_equal(qubit.rho, expected_rho)
    
    assert qubit.measure_prob_0() == 1.0

def test_t1_decay():
    """
    Initialize in |1> state and wait for T1 duration.
    Population of |1> should decay to 1/e (~0.368).
    """
    t1 = 100.0
    qubit = VirtualQubit(t1_us=t1, t2_us=1000.0, frequency_ghz=5.0)
    
    # Set to |1>
    qubit.set_state(0, 1)
    assert qubit.measure_prob_0() == 0.0
    
    # Wait for T1
    qubit.apply_idle_noise(int(t1 * 1000))
    
    # rho_11(t) = rho_11(0) * exp(-t/T1) = 1 * exp(-1) = 1/e
    expected_prob_1 = np.exp(-1)
    expected_prob_0 = 1.0 - expected_prob_1
    
    # print(f"Actual prob_0: {qubit.measure_prob_0()}, Expected: {expected_prob_0}")
    assert np.isclose(qubit.measure_prob_0(), expected_prob_0, atol=1e-5)

def test_t2_decay_superposition():
    """
    Initialize in |+> state and wait for T2 duration.
    Off-diagonal terms (coherence) should decay by 1/e.
    """
    t2 = 50.0
    # Make T1 very large to isolate T2 effects
    qubit = VirtualQubit(t1_us=1e6, t2_us=t2, frequency_ghz=5.0)
    
    # Set to |+> = (|0> + |1>) / sqrt(2)
    qubit.set_state(1/np.sqrt(2), 1/np.sqrt(2))
    
    # Initial coherence rho_01 should be 0.5
    assert np.isclose(qubit.rho[0, 1], 0.5)
    
    # Wait for T2
    qubit.apply_idle_noise(int(t2 * 1000))
    
    # rho_01(t) = rho_01(0) * exp(-t/T2) = 0.5 * exp(-1)
    expected_coherence = 0.5 * np.exp(-1)
    
    assert np.isclose(qubit.rho[0, 1], expected_coherence, atol=1e-5)
    
    # Fidelity check: Should drop significantly from 1.0
    # Original state |+>
    fid = qubit.get_fidelity(1/np.sqrt(2), 1/np.sqrt(2))
    assert fid < 0.9  # Should have degraded
