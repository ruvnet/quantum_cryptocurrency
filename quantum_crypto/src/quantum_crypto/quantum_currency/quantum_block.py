from .quantum_hash import quantum_hash
from .quantum_merkle_tree import build_quantum_merkle_tree, generate_quantum_proof
import time

def create_quantum_block(transactions, previous_hash):
    # Create block with actual transaction data
    block = {
        'transactions': transactions,
        'quantum_proof': f"QPROOF_{abs(hash(str(transactions)))}", # Simple hash for now
        'timestamp': time.time(),
        'previous_hash': previous_hash,
        'block_height': 0  # Will be set by storage
    }
    return block
