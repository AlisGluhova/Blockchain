# Description: This program simulates a blockchain

# Import the library
import hashlib


# Create a block class
class Block:
    # Create a constructor for the Block class
    def __init__(self, data, prev_hash):
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    # Create a method that calculates the hash using SHA256

    def calc_hash(self):
        sha = hashlib.sha256()
        sha.update(self.data.encode('utf-8'))
        return sha.hexdigest()


# create the blockchain class
class Blockchain:
    # create a constructor for the blockain class
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # create a method that creates the first block in the blockchain (aka Genesis block)
    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    # create a method that creates a  new block and adds blocks to the chain(aka the list)
    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(data, prev_block.hash)
        self.chain.append(new_block)


# test the blockchain
blockchain = Blockchain()

# add blocks to the blockchain
blockchain.add_block('First Block')
blockchain.add_block('Second Block')
blockchain.add_block('Third Block')

# print and show the blockchain
print("Blokchain:")
for block in blockchain.chain:
    print("Data:", block.data)
    print("Previous Hash:", block.prev_hash)
    print("Hash:", block.hash)
    print()
