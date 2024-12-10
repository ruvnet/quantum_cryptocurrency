import pytest
from src.quantum_currency.quantum_resource_manager import QuantumResourceManager

def test_resource_allocation():
    """Test quantum resource allocation and limits"""
    qrm = QuantumResourceManager(qubits=5, coherence_time=100, error_correction=True)
    state = qrm.initialize_quantum_state("test_data")
    assert state is not None, "Quantum state should be initialized"

def test_error_correction():
    """Test error correction capabilities"""
    qrm = QuantumResourceManager(qubits=5, coherence_time=100, error_correction=True)
    state = qrm.initialize_quantum_state("test_data")
    noisy_state = introduce_noise(state)  # Simulate noise
    corrected_state = qrm.apply_error_correction(noisy_state)
    assert corrected_state != noisy_state, "Error correction should modify noisy state"

def test_coherence_time_management():
    """Test handling of coherence time constraints"""
    qrm = QuantumResourceManager(qubits=5, coherence_time=50, error_correction=True)
    with pytest.raises(TimeoutError):
        # Simulate operation that exceeds coherence time
        qrm.long_running_operation()

def test_resource_cleanup():
    """Test proper cleanup of quantum resources"""
    qrm = QuantumResourceManager(qubits=5, coherence_time=100, error_correction=True)
    state = qrm.initialize_quantum_state("test_data")
    qrm.cleanup_resources()
    assert qrm.active_states == 0, "All quantum states should be cleaned up"
