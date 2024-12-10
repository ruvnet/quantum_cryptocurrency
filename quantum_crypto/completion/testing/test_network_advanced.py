import pytest
import socket
from src.classical_integration.network import Network
from src.classical_integration.node import Node

def test_peer_connection_management():
    """Test peer connection handling and management"""
    network = Network(Node())
    # Start a test server first
    test_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_server.bind(('localhost', 8398))
    test_server.listen(1)
    
    try:
        network.connect_to_peer('localhost', 8398)
        assert len(network.peers) == 1
    finally:
        test_server.close()
        for peer in network.peers:
            peer.close()
    
def test_broadcast_mechanism():
    """Test broadcasting data to all peers"""
    network = Network(Node())
    test_data = b"test_broadcast_data"
    network.broadcast(test_data)
    
def test_network_resilience():
    """Test network behavior with failing peers"""
    network = Network(Node())
    # Create a peer that will fail
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    network.peers.append(peer)
    # Test broadcast with failing peer
    network.broadcast(b"test_data")
    assert len(network.peers) == 0  # Peer should be removed after failure
