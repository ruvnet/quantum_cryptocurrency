from classical_integration.node import Node
from classical_integration.network import Network
from classical_integration.transactions import create_transaction
import time

def main():
    print("Starting Quantum Cryptocurrency Node...")
    
    # Initialize node and network
    node = Node()
    network = Network(node)
    network.start_server()
    
    # Wait a moment for server to start
    time.sleep(1)
    
    print("Creating sample transactions...")
    
    # Create sample transactions
    tx1 = create_transaction('alice_pubkey', 'bob_pubkey', 10, 'alice_signature')
    tx2 = create_transaction('carol_pubkey', 'dave_pubkey', 20, 'carol_signature')

    # Add transactions to node
    node.add_transaction(tx1)
    node.add_transaction(tx2)

    print("Creating new block...")
    
    try:
        # Create and append a new block
        block = node.create_block()
        print("✅ New block created successfully!")
        print("\nNode is running and ready for connections...")
        
        # Keep the program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down node...")
        exit(0)

if __name__ == "__main__":
    main()
