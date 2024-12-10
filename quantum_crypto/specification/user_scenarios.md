# User Scenarios

## Scenario 1: User Registration
- **Actors**: New User
- **Description**: A new user registers on the platform, generating a quantum-resistant key pair.
- **Steps**:
  1. User initiates registration.
  2. System generates a lattice-based private key.
  3. System derives the corresponding public key.
  4. User receives their public key and securely stores the private key.

## Scenario 2: Transaction Creation
- **Actors**: Registered User
- **Description**: A user creates and broadcasts a transaction to transfer quantum currency.
- **Steps**:
  1. User initiates a transaction specifying sender, receiver, and amount.
  2. System signs the transaction with the sender's private key.
  3. System hashes the transaction using the quantum hashing function.
  4. Transaction is broadcasted to the network for inclusion in a block.

## Scenario 3: Block Validation
- **Actors**: Network Node
- **Description**: A node validates a newly received block using quantum proof.
- **Steps**:
  1. Node receives a new block.
  2. Node verifies the quantum proof against the transaction hashes.
  3. If valid, the block is appended to the local blockchain.
  4. Node broadcasts the validated block to other peers.
