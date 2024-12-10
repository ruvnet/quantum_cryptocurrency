import pytest
from src.quantum_currency.quantum_consensus import validate_block, verify_quantum_proof
from src.classical_integration.node import Node
from src.classical_integration.transactions import create_transaction

def test_block_validation():
    """Test complete block validation process"""
    node = Node()
    tx = create_transaction('alice', 'bob', 100, 'sig123')
    node.add_transaction(tx)
    block = node.create_block()
    
    assert validate_block(block), "Valid block should pass validation"
    assert verify_quantum_proof(block['quantum_proof'], block['transactions']), "Quantum proof should verify"

def test_invalid_block_structure():
    """Test rejection of malformed blocks"""
    invalid_block = {
        'transactions': [],  # Empty transactions
        'timestamp': 123456789
        # Missing required fields
    }
    assert not validate_block(invalid_block), "Invalid block should fail validation"

def test_consensus_agreement():
    """Test consensus agreement among multiple nodes"""
    nodes = [Node() for _ in range(3)]
    tx = create_transaction('alice', 'bob', 100, 'sig123')
    
    # Add same transaction to all nodes
    for node in nodes:
        node.add_transaction(tx)
    
    # Create blocks on each node
    blocks = [node.create_block() for node in nodes]
    
    # All nodes should agree on block validity
    consensus = all(node.validate_block(blocks[0]) for node in nodes)
    assert consensus, "All nodes should agree on block validity"
