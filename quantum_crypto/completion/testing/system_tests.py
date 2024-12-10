import pytest
from src.classical_integration.node import Node
from src.classical_integration.transactions import create_transaction

def test_end_to_end_transaction_validation():
    node = Node()
    tx1 = create_transaction('alice', 'bob', 10, 'sig1')
    tx2 = create_transaction('carol', 'dave', 20, 'sig2')
    
    node.add_transaction(tx1)
    node.add_transaction(tx2)
    
    block = node.create_block()
    valid = node.validate_block(block)
    
    assert valid, "Block should be valid and appended to the ledger"
