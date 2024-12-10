import pytest
from src.quantum_currency.quantum_hash import quantum_hash

def test_hash_determinism():
    tx_data = "sender=alice&receiver=bob&amount=10"
    result1 = quantum_hash(tx_data)
    result2 = quantum_hash(tx_data)
    assert result1 == result2, "Quantum hash should produce consistent results"
