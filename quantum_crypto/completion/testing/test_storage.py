import pytest
from src.classical_integration.storage import Storage
import os

def test_blockchain_persistence():
    """Test blockchain data persistence"""
    storage = Storage('test_blockchain.json')
    block = {
        'transactions': [{'sender': 'alice', 'receiver': 'bob', 'amount': 10}],
        'quantum_proof': 'test_proof',
        'timestamp': 123456789,
        'previous_hash': 'prev_hash'
    }
    stored_block = storage.append_block(block)
    assert stored_block['block_height'] == 0
    
    # Reload storage and verify
    new_storage = Storage('test_blockchain.json')
    chain = new_storage.get_blockchain()
    assert len(chain) == 1
    assert chain[0]['quantum_proof'] == 'test_proof'

def test_concurrent_access():
    """Test concurrent access to storage"""
    storage = Storage('test_blockchain.json')
    # Simulate concurrent writes
    block1 = {'transactions': [], 'quantum_proof': 'proof1', 'timestamp': 1, 'previous_hash': 'hash1'}
    block2 = {'transactions': [], 'quantum_proof': 'proof2', 'timestamp': 2, 'previous_hash': 'hash2'}
    storage.append_block(block1)
    storage.append_block(block2)
    assert storage.get_last_block_hash() == 'proof2'

@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test files after each test"""
    yield
    if os.path.exists('test_blockchain.json'):
        os.remove('test_blockchain.json')
