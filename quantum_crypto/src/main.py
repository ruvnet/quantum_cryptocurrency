from classical_integration.node import Node
from classical_integration.network import Network
from classical_integration.transactions import create_transaction

def main():
    node = Node()
    network = Network(node)
    network.start_server()

    # Example transactions
    tx1 = create_transaction('alice_pubkey', 'bob_pubkey', 10, 'alice_signature')
    tx2 = create_transaction('carol_pubkey', 'dave_pubkey', 20, 'carol_signature')

    node.add_transaction(tx1)
    node.add_transaction(tx2)

    # Create and append a new block
    block = node.create_block()
    print("New block created and appended:", block)

if __name__ == "__main__":
    main()
