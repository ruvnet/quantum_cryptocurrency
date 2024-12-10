# System Architecture

## Components
1. **Quantum Resource Manager**: 
   Interfaces with the Willow chip for state initialization, gate application, and measurement.
2. **Quantum-Currency Module**:
   - quantum_keygen.py: Handles post-quantum key generation.
   - quantum_hash.py: Implements quantum hashing.
   - quantum_merkle_tree.py: Builds and verifies quantum Merkle proofs.
   - quantum_block.py: Creates and assembles blocks with quantum proofs.
   - quantum_consensus.py: Defines a quantum-aware consensus mechanism.
3. **Classical Integration Layer**:
   - node.py: Represents a node in the network, handling incoming blocks and broadcasting.
   - network.py: Manages P2P communication among nodes.
   - storage.py: Manages local state and ledger storage (blockchain data).
   - transactions.py: Manages creation, validation, and serialization of transactions.

## Data Flow
- User generates transaction using quantum-resistant keys.
- Transaction data is hashed by quantum_hash.py.
- Blocks are formed by quantum_block.py, utilizing quantum_merkle_tree.py for proofs.
- Nodes (classical) validate blocks, possibly delegating quantum verification to trusted quantum validators.
- Validated blocks are appended to the ledger in storage.py.
