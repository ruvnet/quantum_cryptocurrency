import pytest
from src.classical_integration.node import Node
from src.classical_integration.transactions import create_transaction
from src.quantum_currency.quantum_block import create_quantum_block
from src.quantum_currency.quantum_consensus import validate_block

def test_end_to_end_transaction_validation():
    """Test complete flow from transaction creation to block validation"""
    node = Node()
    tx1 = create_transaction('alice', 'bob', 10, 'sig1')
    tx2 = create_transaction('carol', 'dave', 20, 'sig2')
    
    node.add_transaction(tx1)
    node.add_transaction(tx2)
    
    block = node.create_block()
    valid = node.validate_block(block)
    
    assert valid, "Block should be valid and appended to the ledger"
    assert len(block['transactions']) == 2, "Block should contain both transactions"
    assert block['quantum_proof'].startswith("QPROOF_"), "Block should have quantum proof"

def test_multiple_block_creation():
    """Test creating multiple blocks and maintaining chain integrity"""
    node = Node()
    
    # Create first block
    tx1 = create_transaction('alice', 'bob', 10, 'sig1')
    node.add_transaction(tx1)
    block1 = node.create_block()
    
    # Create second block
    tx2 = create_transaction('carol', 'dave', 20, 'sig2')
    node.add_transaction(tx2)
    block2 = node.create_block()
    
    assert block2['previous_hash'] == block1['quantum_proof'], "Block chain should be properly linked"
    assert block2['block_height'] > block1['block_height'], "Block height should increase"

def test_invalid_block_rejection():
    """Test that invalid blocks are rejected"""
    node = Node()
    
    # Create invalid block (empty transactions)
    with pytest.raises(ValueError):
        node.create_block()
