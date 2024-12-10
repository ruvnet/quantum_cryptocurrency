import pytest
import time
from quantum_crypto.quantum_currency.quantum_hash import quantum_hash
from quantum_crypto.quantum_currency.quantum_keygen import (
    generate_quantum_keypair,
    sign_message,
    verify_signature
)

class TestTransaction:
    @pytest.fixture
    def keypair(self):
        """Generate a test keypair"""
        return generate_quantum_keypair()

    @pytest.fixture
    def transaction(self, keypair):
        """Create a test transaction"""
        public_key, private_key = keypair
        return {
            'sender': public_key,
            'recipient': b'recipient_address',
            'amount': 100,
            'timestamp': int(time.time()),
            'nonce': 0
        }

    def test_transaction_hash(self, transaction):
        """Test transaction hashing"""
        tx_bytes = self._transaction_to_bytes(transaction)
        tx_hash = quantum_hash(tx_bytes)
        
        assert isinstance(tx_hash, bytes)
        assert len(tx_hash) > 0

    def test_transaction_signing(self, transaction, keypair):
        """Test transaction signing and verification"""
        public_key, private_key = keypair
        tx_bytes = self._transaction_to_bytes(transaction)
        
        # Sign transaction
        signature = sign_message(tx_bytes, private_key)
        assert isinstance(signature, bytes)
        
        # Verify signature
        is_valid = verify_signature(tx_bytes, signature, public_key)
        assert is_valid

    def test_invalid_transaction(self, transaction, keypair):
        """Test invalid transaction detection"""
        public_key, private_key = keypair
        tx_bytes = self._transaction_to_bytes(transaction)
        
        # Sign original transaction
        signature = sign_message(tx_bytes, private_key)
        
        # Modify transaction
        transaction['amount'] = 200
        modified_tx_bytes = self._transaction_to_bytes(transaction)
        
        # Verify with modified transaction
        is_valid = verify_signature(modified_tx_bytes, signature, public_key)
        assert not is_valid

    def test_double_spend(self, transaction, keypair):
        """Test double spend detection"""
        public_key, private_key = keypair
        tx_bytes = self._transaction_to_bytes(transaction)
        
        # Create two identical transactions
        signature1 = sign_message(tx_bytes, private_key)
        hash1 = quantum_hash(tx_bytes + signature1)
        
        # Increment nonce for second transaction
        transaction['nonce'] += 1
        tx_bytes2 = self._transaction_to_bytes(transaction)
        signature2 = sign_message(tx_bytes2, private_key)
        hash2 = quantum_hash(tx_bytes2 + signature2)
        
        # Hashes should be different
        assert hash1 != hash2

    def _transaction_to_bytes(self, tx):
        """Convert transaction dict to bytes"""
        components = [
            tx['sender'],
            tx['recipient'],
            str(tx['amount']).encode(),
            str(tx['timestamp']).encode(),
            str(tx['nonce']).encode()
        ]
        return b'|'.join(components)
