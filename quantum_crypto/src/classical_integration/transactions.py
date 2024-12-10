import hashlib

class Transaction:
    def __init__(self, sender_pubkey, receiver_pubkey, amount, signature):
        self.sender = sender_pubkey
        self.receiver = receiver_pubkey
        self.amount = amount
        self.signature = signature
        self.txid = None  # Will be generated by quantum_hash

def create_transaction(sender, receiver, amount, signature):
    return {
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'signature': signature
    }

def serialize(transaction):
    return f"{transaction['sender']}{transaction['receiver']}{transaction['amount']}{transaction['signature']}"