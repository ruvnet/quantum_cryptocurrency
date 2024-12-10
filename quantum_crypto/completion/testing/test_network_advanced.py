import pytest
from src.classical_integration.network import Network
from src.classical_integration.node import Node

def test_peer_connection_management():
    """Test peer connection handling and management"""
    network = Network(Node())
    network.connect_to_peer('localhost', 8334)
    assert len(network.peers) == 1
    
def test_broadcast_mechanism():
    """Test broadcasting data to all peers"""
    network = Network(Node())
    test_data = b"test_broadcast_data"
    network.broadcast(test_data)
    
def test_network_resilience():
    """Test network behavior with failing peers"""
    network = Network(Node())
    # Add multiple peers and simulate some failing
    network.connect_to_peer('localhost', 8334)
    network.connect_to_peer('localhost', 8335)
    # Simulate peer failure
    network.peers[0].close()
    network.broadcast(b"test_data")
    assert len(network.peers) == 1  # Should remove failed peer
