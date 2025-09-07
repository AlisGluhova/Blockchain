from ecdsa import SigningKey, SECP256k1


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

    print('test')
