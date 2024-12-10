import pytest
import socket
import threading
import time
from src.classical_integration.network import Network
from src.classical_integration.node import Node

@pytest.fixture
def test_node():
    return Node()

@pytest.fixture
def test_network(test_node):
    return Network(test_node)

def test_network_initialization(test_network):
    """Test network object initialization"""
    assert isinstance(test_network.server, socket.socket)
    assert test_network.peers == []
    assert isinstance(test_network.node, Node)

def test_server_start(test_network):
    """Test server starts and listens on specified port"""
    test_port = 8399  # Use a less common port for testing
    
    # Configure server socket with SO_REUSEADDR
    test_network.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    test_network.start_server(port=test_port)
    
    # Give server time to start
    time.sleep(0.1)
    
    # Try connecting to server
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        test_socket.connect(('localhost', test_port))
        connection_successful = True
    except:
        connection_successful = False
    finally:
        test_socket.close()
        # Properly shutdown the server socket
        test_network.server.shutdown(socket.SHUT_RDWR)
        test_network.server.close()
    
    assert connection_successful, "Server should accept connections"
