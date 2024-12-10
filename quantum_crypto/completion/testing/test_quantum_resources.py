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
    # Simulate noise by flipping some qubits
    noisy_state = qrm.simulate_noise(state)
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

def test_quantum_state_initialization_limits():
    """Test quantum state initialization limits"""
    qrm = QuantumResourceManager(qubits=3, coherence_time=100, error_correction=True)
    state1 = qrm.initialize_quantum_state("data1")
    state2 = qrm.initialize_quantum_state("data2")
    state3 = qrm.initialize_quantum_state("data3")
    assert qrm.active_states == 3
    
def test_gate_application_sequence():
    """Test quantum gate application sequence"""
    qrm = QuantumResourceManager(qubits=5, coherence_time=100, error_correction=True)
    state = qrm.initialize_quantum_state("test_data")
    gates = ['H', 'CNOT', 'T', 'S']
    transformed_state = qrm.apply_gates(state, gates)
    assert transformed_state != state

def test_error_correction_threshold():
    """Test error correction activation threshold"""
    qrm = QuantumResourceManager(qubits=5, coherence_time=100, error_correction=True)
    state = qrm.initialize_quantum_state("test_data")
    noisy_state = qrm.simulate_noise(state)
    corrected_state = qrm.apply_error_correction(noisy_state)
    assert corrected_state.endswith('_corrected')
