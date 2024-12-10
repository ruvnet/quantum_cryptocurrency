from ..quantum_currency.quantum_block import create_quantum_block
from ..quantum_currency.quantum_consensus import validate_block
from .transactions import Transaction
from .storage import Storage

class Node:
    def __init__(self):
        self.storage = Storage()
        self.pending_transactions = []

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        print(f"➕ Transaction added to pending pool. Total pending: {len(self.pending_transactions)}")

    def create_block(self):
        if not self.pending_transactions:
            raise ValueError("No pending transactions to create block")
            
        print(f"📦 Creating new block with {len(self.pending_transactions)} transactions")
        previous_hash = self.storage.get_last_block_hash()
        
        print("⚙️ Generating quantum proof...")
        block = create_quantum_block(self.pending_transactions, previous_hash)
        
        print("🔍 Validating block...")
        if validate_block(block):
            stored_block = self.storage.append_block(block)
            self.pending_transactions = []  # Clear pending after successful creation
            return stored_block
        else:
            raise ValueError("❌ Block validation failed")

    def validate_block(self, block):
        return validate_block(block)
