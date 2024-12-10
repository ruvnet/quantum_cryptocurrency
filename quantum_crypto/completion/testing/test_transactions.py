import pytest
from src.classical_integration.transactions import create_transaction, serialize
from src.quantum_currency.quantum_hash import quantum_hash

def test_transaction_creation():
    """Test transaction creation with required fields"""
    tx = create_transaction('sender123', 'receiver456', 100, 'signature789')
    assert tx['sender'] == 'sender123'
    assert tx['receiver'] == 'receiver456'
    assert tx['amount'] == 100
    assert tx['signature'] == 'signature789'

def test_transaction_serialization():
    """Test transaction serialization for hashing"""
    tx = create_transaction('alice', 'bob', 50, 'sig123')
    serialized = serialize(tx)
    assert isinstance(serialized, str), "Serialized output should be string"
    assert 'alice' in serialized
    assert 'bob' in serialized
    assert '50' in serialized

def test_invalid_transaction_amount():
    """Test handling of invalid transaction amounts"""
    with pytest.raises(ValueError):
        create_transaction('alice', 'bob', -10, 'sig123')

def test_duplicate_transaction_detection():
    """Test detection of duplicate transactions"""
    tx1 = create_transaction('alice', 'bob', 100, 'sig123')
    tx2 = create_transaction('alice', 'bob', 100, 'sig123')
    hash1 = quantum_hash(serialize(tx1))
    hash2 = quantum_hash(serialize(tx2))
    assert hash1 == hash2, "Identical transactions should have same hash"
