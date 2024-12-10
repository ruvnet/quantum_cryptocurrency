from .quantum_hash import quantum_hash
from .quantum_merkle_tree import build_quantum_merkle_tree, generate_quantum_proof
import time

def create_quantum_block(transactions, previous_hash):
    for tx in transactions:
        tx_data = f"{tx['sender']}{tx['receiver']}{tx['amount']}{tx['signature']}"
        tx['txid'] = quantum_hash(tx_data)
    merkle_root = build_quantum_merkle_tree([tx['txid'] for tx in transactions])
    quantum_proof = generate_quantum_proof(merkle_root)

    return {
        'transactions': transactions,
        'quantum_proof': quantum_proof,
        'timestamp': time.time(),
        'previous_hash': previous_hash
    }
