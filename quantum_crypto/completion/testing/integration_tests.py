import unittest
from src.quantum_currency.quantum_hash import quantum_hash
from src.quantum_currency.quantum_merkle_tree import build_quantum_merkle_tree, generate_quantum_proof
from src.quantum_currency.quantum_block import create_quantum_block

class TestIntegration(unittest.TestCase):
    def test_transaction_to_block_flow(self):
        transactions = [
            {'sender': 'alice', 'receiver': 'bob', 'amount': 10, 'signature': 'sig1'},
            {'sender': 'carol', 'receiver': 'dave', 'amount': 20, 'signature': 'sig2'}
        ]
        previous_hash = "PREV_HASH_12345"
        block = create_quantum_block(transactions, previous_hash)
        
        self.assertEqual(block['previous_hash'], previous_hash, "Previous hash should match")
        self.assertEqual(len(block['transactions']), 2, "Block should contain two transactions")
        self.assertTrue(block['quantum_proof'].startswith("QPROOF_"), "Quantum proof should have correct prefix")

if __name__ == '__main__':
    unittest.main()
