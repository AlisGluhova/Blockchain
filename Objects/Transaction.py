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
