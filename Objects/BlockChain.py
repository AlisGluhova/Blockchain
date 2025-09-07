from Objects.Block import Block


class Blockchain:

    def __init__(self):
        self.chain = [Block(["Genesis Block"], "0")]

    def lenght(self):
        return len(self.chain)