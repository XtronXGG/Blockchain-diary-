import hashlib
import time
import uuid

class Block:
    def __init__(self, index, timestamp, user, title, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.user = user
        self.title = title
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.diary_id = str(uuid.uuid4())  # unique diary ID

    def calculate_hash(self):
        block_string = (
            str(self.index) + str(self.timestamp) + self.user + self.title +
            self.data + self.previous_hash
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.ctime(), "System", "Genesis Block", "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, user, title, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.ctime(), user, title, data, latest_block.hash)
        self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            if current.previous_hash != prev.hash:
                return False
            if current.hash != current.calculate_hash():
                return False
        return True
