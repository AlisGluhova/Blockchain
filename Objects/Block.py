import hashlib


class Block:
    def __init__(self, transactions, prev_hash):
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.transactions) + self.prev_hash).encode('utf-8'))
        return sha.hexdigest()
