import json
import os

class Storage:
    def __init__(self, storage_file='blockchain.json'):
        self.storage_file = storage_file
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)

    def append_block(self, block):
        blockchain = self.get_blockchain()
        # Set block height
        block['block_height'] = len(blockchain)
        blockchain.append(block)
        with open(self.storage_file, 'w') as f:
            json.dump(blockchain, f, indent=4)
        print(f"Block #{block['block_height']} added to chain")
        return block

    def get_blockchain(self):
        with open(self.storage_file, 'r') as f:
            return json.load(f)

    def get_last_block_hash(self):
        blockchain = self.get_blockchain()
        if blockchain:
            return blockchain[-1]['quantum_proof']
        return "GENESIS_HASH"
