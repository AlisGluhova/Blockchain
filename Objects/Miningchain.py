from Objects.BlockChain import Blockchain
from Objects.Transaction import Transaction
from Objects.Block import Block


class MiningChain(Blockchain):
    MINING_REWARD = 10

    def __init__(self):
        super().__init__()
        self.pending_transactions = []
        self.balances = {}

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
