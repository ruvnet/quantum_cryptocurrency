import unittest
from src.quantum_currency.quantum_hash import quantum_hash

class TestQuantumHash(unittest.TestCase):
    def test_hash_determinism(self):
        tx_data = "sender=alice&receiver=bob&amount=10"
        result1 = quantum_hash(tx_data)
        result2 = quantum_hash(tx_data)
        self.assertEqual(result1, result2, "Quantum hash should produce consistent results")

if __name__ == '__main__':
    unittest.main()
