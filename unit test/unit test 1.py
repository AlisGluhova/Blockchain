import unittest
from Objects.BlockChain import Blockchain
from Objects.Miningchain import MiningChain
from ecdsa import SigningKey, SECP256k1


class BlockchainTest(unittest.TestCase):
    def test_something(self):
        blockchain = Blockchain()

        chain_lenght = blockchain.lenght()

        print(chain_lenght)

        self.assertEqual(1, chain_lenght)


class MiningTest(unittest.TestCase):
    def test_something(self):
        miningchain = MiningChain()
        alice_private = SigningKey.generate(curve=SECP256k1)
        alice_public = alice_private.verifying_key

        miningchain.mine_block(alice_public.to_string().hex())

        chain_lenght = miningchain.lenght()

        self.assertEqual(2, chain_lenght)


if __name__ == '__main__':
    unittest.main()
