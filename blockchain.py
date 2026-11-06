import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = {
            "index": 1,
            "timestamp": 0,
            "transactions": [],
            "nonce": 0,
            "previous_hash": "0" * 64,
        }
        self.chain.append(genesis)

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": transactions,
            "nonce": 0,
            "previous_hash": self.hash(self.last_block),
        }
        self.chain.append(block)
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            previous = self.chain[i - 1]
            current = self.chain[i]
            if current["previous_hash"] != self.hash(previous):
                return False, current["index"]
            if current["index"] != previous["index"] + 1:
                return False, current["index"]
        return True, None

    def print_chain(self):
        for block in self.chain:
            print(json.dumps(block, indent=2, ensure_ascii=False))
            print("hash:", self.hash(block))
            print("-" * 70)


if __name__ == "__main__":
    bc = Blockchain()
    bc.add_block(["Alice -> Bob: 5"])
    bc.add_block(["Bob -> Carol: 2"])
    bc.add_block(["Carol -> Dave: 1", "Dave -> Alice: 3"])
    bc.print_chain()

    for i in range(1, len(bc.chain)):
        ok = bc.chain[i]["previous_hash"] == Blockchain.hash(bc.chain[i - 1])
        print(f"Blok {i + 1}: previous_hash == hash(blok {i}) -> {ok}")
