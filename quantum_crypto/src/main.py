from quantum_crypto.classical_integration.node import Node
from quantum_crypto.classical_integration.network import Network
from quantum_crypto.classical_integration.transactions import create_transaction
import time

def main():
    print("\n🚀 Starting Quantum Cryptocurrency Node...")
    
    # Initialize node and network
    node = Node()
    network = Network(node)
    network.start_server()
    
    # Wait a moment for server to start
    time.sleep(1)
    
    print("\n📝 Creating sample transactions...")
    
    # Create sample transactions with more details
    tx1 = create_transaction('alice_pubkey', 'bob_pubkey', 10, 'alice_signature')
    tx2 = create_transaction('carol_pubkey', 'dave_pubkey', 20, 'carol_signature')

    # Add transactions to node
    node.add_transaction(tx1)
    node.add_transaction(tx2)

    print("\n🔨 Creating new block...")
    
    try:
        # Create and append a new block
        block = node.create_block()
        
        # Print detailed block information
        print("\n✅ New block created successfully!")
        print("\n📦 Block Details:")
        print(f"├── Height: #{block['block_height']}")
        print(f"├── Timestamp: {time.ctime(block['timestamp'])}")
        print(f"├── Previous Hash: {block['previous_hash']}")
        print(f"├── Quantum Proof: {block['quantum_proof']}")
        print(f"└── Transactions: {len(block['transactions'])} total")
        
        # Print transaction details
        print("\n💰 Transaction Details:")
        for idx, tx in enumerate(block['transactions'], 1):
            print(f"Transaction #{idx}:")
            print(f"├── From: {tx['sender']}")
            print(f"├── To: {tx['receiver']}")
            print(f"└── Amount: {tx['amount']} QC")  # QC for Quantum Coins
        
        print("\n🔄 Node is running and ready for connections...")
        
        # Keep the program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down node...")
        exit(0)

if __name__ == "__main__":
    main()
