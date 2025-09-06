import hashlib
from ecdsa import SigningKey, SECP256k1


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }

    # signing the transaction using private key
    def sign_transaction(self, private_key):
        message = str(self.to_dict()).encode()
        self.signature = private_key.sign(message).hex()

    # verifying the signature using the public key
    def is_valid(self, public_key):
        if self.sender == "MINING":
            return True
        message = str(self.to_dict()).encode()
        try:
            return public_key.verify(bytes.fromhex(self.signature), message)

        except:
            return False

    def __repr__(self):
        return f"{self.sender[:10]} -> {self.recipient[:10]}: {self.amount}"


class Block:
    def __init__(self, transactions, prev_hash):
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.transactions) + self.prev_hash).encode('utf-8'))
        return sha.hexdigest()


class Blockchain:
    MINING_REWARD = 10

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.balances = {}

    def create_genesis_block(self):
        return Block(["Genesis Block"], "0")

    def add_transaction(self, tx, sender_public_key=None):
        if tx.sender == "MINING":
            self.pending_transactions.append(tx)
            return True

        if not tx.is_valid(sender_public_key):
            print("Invalid transaction! Signature check failed.")
            return False

        if self.balances.get(tx.sender, 0) < tx.amount:
            print(f"Transaction invalid: {tx.sender} doesn't have enough balance!")
            return False

        self.pending_transactions.append(tx)
        return True

    def mine_block(self, miner_address):
        reward_tx = Transaction("MINING", miner_address, self.MINING_REWARD)
        self.pending_transactions.append(reward_tx)

        prev_block = self.chain[-1]
        new_block = Block(self.pending_transactions, prev_block.hash)
        self.chain.append(new_block)

        for tx in self.pending_transactions:
            self.apply_transaction(tx)

        self.pending_transactions = []

    def apply_transaction(self, tx):
        if tx.sender != "MINING":
            if self.balances.get(tx.sender, 0) < tx.amount:
                print(f"Transaction invalid: {tx.sender} has insufficient funds!")
                return False
            self.balances[tx.sender] -= tx.amount

        self.balances[tx.recipient] = self.balances.get(tx.recipient, 0) + tx.amount
        return True


# Demo

if __name__ == "__main__":
    # Create wallets
    alice_private = SigningKey.generate(curve=SECP256k1)
    alice_public = alice_private.verifying_key

    bob_private = SigningKey.generate(curve=SECP256k1)
    bob_public = bob_private.verifying_key

    # Blockchain instance
    blockchain = Blockchain()

    # Mine first block (Alice mines, gets 10 coins)
    blockchain.mine_block(alice_public.to_string().hex())

    # Alice sends 5 coins to Bob
    tx1 = Transaction(alice_public.to_string().hex(), bob_public.to_string().hex(), 5)
    tx1.sign_transaction(alice_private)
    blockchain.add_transaction(tx1, alice_public)
    blockchain.mine_block(bob_public.to_string().hex())  # Bob mines next block

    # Bob tries to overspend (invalid)
    tx2 = Transaction(bob_public.to_string().hex(), alice_public.to_string().hex(), 20)
    tx2.sign_transaction(bob_private)
    blockchain.add_transaction(tx2, bob_public)  # This should fail
    blockchain.mine_block(alice_public.to_string().hex())

    # Print balances
    print("\n💰 Final Balances:")
    for wallet, balance in blockchain.balances.items():
        print(wallet[:10], ":", balance)

    # Print blockchain
    print("\n📜 Blockchain:")
    for block in blockchain.chain:
        print("Transactions:", block.transactions)
        print("Previous Hash:", block.prev_hash)
        print("Hash:", block.hash)
        print()

