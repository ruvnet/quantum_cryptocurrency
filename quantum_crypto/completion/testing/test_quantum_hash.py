import pytest
from src.quantum_currency.quantum_hash import quantum_hash
from src.quantum_currency.quantum_resource_manager import QuantumResourceManager

def test_quantum_hash_deterministic():
    """Test that quantum hash produces consistent results for same input"""
    data1 = "test_transaction_data"
    data2 = "test_transaction_data"
    
    hash1 = quantum_hash(data1)
    hash2 = quantum_hash(data2)
    
    assert hash1 == hash2, "Quantum hash should be deterministic for same input"

def test_quantum_hash_different_inputs():
    """Test that different inputs produce different hashes"""
    data1 = "transaction1"
    data2 = "transaction2"
    
    hash1 = quantum_hash(data1)
    hash2 = quantum_hash(data2)
    
    assert hash1 != hash2, "Different inputs should produce different hashes"

def test_quantum_resource_manager_initialization():
    """Test quantum resource manager initialization"""
    qrm = QuantumResourceManager(qubits=5, coherence_time=100, error_correction=True)
    assert qrm.qubits == 5
    assert qrm.coherence_time == 100
    assert qrm.error_correction == True
