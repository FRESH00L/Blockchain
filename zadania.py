import hashlib
import json

from blockchain import Blockchain


def hash_without_sort(block):
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()


def zadanie_sort_keys():
    print("=== 2.2: sort_keys=True a kolejność pól ===")
    block_a = {
        "index": 2,
        "timestamp": 1727251200,
        "transactions": ["Alice -> Bob: 5"],
        "nonce": 0,
        "previous_hash": "0" * 64,
    }
    block_b = {
        "previous_hash": "0" * 64,
        "nonce": 0,
        "transactions": ["Alice -> Bob: 5"],
        "timestamp": 1727251200,
        "index": 2,
    }
    print("block_a == block_b:", block_a == block_b)
    print("bez sort_keys A:", hash_without_sort(block_a))
    print("bez sort_keys B:", hash_without_sort(block_b))
    print("z sort_keys   A:", Blockchain.hash(block_a))
    print("z sort_keys   B:", Blockchain.hash(block_b))
    print()


def build_chain():
    bc = Blockchain()
    bc.add_block(["Alice -> Bob: 5"])
    bc.add_block(["Bob -> Carol: 2"])
    bc.add_block(["Carol -> Dave: 1"])
    return bc


def zadanie_integralnosc():
    print("=== 2.3: weryfikacja integralności ===")
    bc = build_chain()
    print("Łańcuch oryginalny:", bc.is_chain_valid())

    bc.chain[1]["transactions"][0] = "Alice -> Bob: 500"
    print("Po zmianie kwoty w bloku nr 2:", bc.is_chain_valid())

    for i in range(2, len(bc.chain)):
        bc.chain[i]["previous_hash"] = Blockchain.hash(bc.chain[i - 1])
    print("Po przeliczeniu previous_hash przez atakującego:", bc.is_chain_valid())

    bc2 = build_chain()
    bc2.last_block["transactions"][0] = "Carol -> Dave: 1000"
    print("Po zmianie ostatniego bloku:", bc2.is_chain_valid())


if __name__ == "__main__":
    zadanie_sort_keys()
    zadanie_integralnosc()
