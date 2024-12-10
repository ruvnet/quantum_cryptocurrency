import pytest
from src.classical_integration.node import Node
from src.classical_integration.network import Network
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

def test_full_node_lifecycle():
    """Test complete node lifecycle including startup, transaction processing, and shutdown"""
    node = Node()
    network = Network(node)
    network.start_server(port=8336)
    
    # Add transactions
    tx1 = create_transaction('alice', 'bob', 10, 'sig1')
    tx2 = create_transaction('carol', 'dave', 20, 'sig2')
    node.add_transaction(tx1)
    node.add_transaction(tx2)
    
    # Create block
    block = node.create_block()
    
    # Verify block is stored
    assert node.storage.get_last_block_hash() == block['quantum_proof']
    
    # Clean up
    network.server.close()

def test_network_synchronization():
    """Test synchronization between multiple nodes"""
    node1 = Node()
    node2 = Node()
    network1 = Network(node1)
    network2 = Network(node2)
    
    network1.start_server(port=8337)
    network2.start_server(port=8338)
    
    # Connect nodes
    network1.connect_to_peer('localhost', 8338)
    
    # Create transaction on node1
    tx = create_transaction('alice', 'bob', 10, 'sig1')
    node1.add_transaction(tx)
    block = node1.create_block()
    
    # Verify both nodes have the block
    assert node1.storage.get_last_block_hash() == node2.storage.get_last_block_hash()
