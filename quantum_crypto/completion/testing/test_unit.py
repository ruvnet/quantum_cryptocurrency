import pytest
from quantum_crypto.src.quantum_currency.quantum_hash import quantum_hash

def test_hash_determinism():
    tx_data = "sender=alice&receiver=bob&amount=10"
    result1 = quantum_hash(tx_data)
    result2 = quantum_hash(tx_data)
    assert result1 == result2, "Quantum hash should produce consistent results"

def test_hash_different_inputs():
    tx_data1 = "sender=alice&receiver=bob&amount=10"
    tx_data2 = "sender=bob&receiver=alice&amount=10"
    result1 = quantum_hash(tx_data1)
    result2 = quantum_hash(tx_data2)
    assert result1 != result2, "Different inputs should produce different hashes"

def test_hash_format():
    tx_data = "sender=alice&receiver=bob&amount=10"
    result = quantum_hash(tx_data)
    assert result.startswith("QHASH_"), "Hash should start with QHASH_ prefix"
    assert len(result) > 6, "Hash should have sufficient length"
    assert result[6:].isdigit(), "Hash should contain only digits after prefix"
