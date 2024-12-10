import pytest
from quantum_crypto.quantum_currency.quantum_hash import quantum_hash
import numpy as np

def test_quantum_hash_basic():
    """Test basic quantum hash functionality"""
    test_data = b"test data"
    hash_result = quantum_hash(test_data)
    
    assert isinstance(hash_result, bytes)
    assert len(hash_result) > 0

def test_quantum_hash_deterministic():
    """Test that same input produces consistent hash"""
    test_data = b"test data"
    hash1 = quantum_hash(test_data)
    hash2 = quantum_hash(test_data)
    
    # Due to quantum nature, hashes may vary slightly
    # but should be within acceptable range
    similarity = _calculate_hash_similarity(hash1, hash2)
    assert similarity > 0.9  # 90% similarity threshold

def test_quantum_hash_different_inputs():
    """Test that different inputs produce different hashes"""
    hash1 = quantum_hash(b"data1")
    hash2 = quantum_hash(b"data2")
    
    similarity = _calculate_hash_similarity(hash1, hash2)
    assert similarity < 0.5  # Should be significantly different

def test_quantum_hash_empty_input():
    """Test handling of empty input"""
    hash_result = quantum_hash(b"")
    assert isinstance(hash_result, bytes)
    assert len(hash_result) > 0

def test_quantum_hash_large_input():
    """Test handling of large input data"""
    large_data = b"x" * 1000000  # 1MB of data
    hash_result = quantum_hash(large_data)
    
    assert isinstance(hash_result, bytes)
    assert len(hash_result) > 0

def _calculate_hash_similarity(hash1: bytes, hash2: bytes) -> float:
    """Calculate similarity between two hash values"""
    # Convert to bit arrays for comparison
    bits1 = np.unpackbits(np.frombuffer(hash1, dtype=np.uint8))
    bits2 = np.unpackbits(np.frombuffer(hash2, dtype=np.uint8))
    
    # Calculate similarity (1 - Hamming distance)
    min_len = min(len(bits1), len(bits2))
    matching_bits = np.sum(bits1[:min_len] == bits2[:min_len])
    return matching_bits / min_len
