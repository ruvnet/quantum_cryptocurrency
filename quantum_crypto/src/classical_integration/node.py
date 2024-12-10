from src.quantum_currency.quantum_block import create_quantum_block
from src.quantum_currency.quantum_consensus import validate_block
from src.classical_integration.transactions import Transaction
from src.classical_integration.storage import Storage

class Node:
    def __init__(self):
        self.storage = Storage()
        self.pending_transactions = []

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def create_block(self):
        previous_hash = self.storage.get_last_block_hash()
        block = create_quantum_block(self.pending_transactions, previous_hash)
        if validate_block(block):
            self.storage.append_block(block)
            self.pending_transactions = []
            return block
        else:
            raise ValueError("Invalid block")

    def validate_block(self, block):
        return validate_block(block)
