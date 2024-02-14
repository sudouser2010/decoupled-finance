from hashlib import sha512
import json


class Block:
    def __init__(self, index: int, transactions: list[dict], end_timestamp: int, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.end_timestamp = end_timestamp
        self.previous_hash = previous_hash

        # initialize the current hash as None
        self.hash = ''

    def compute_hash(self) -> str:
        """
        Creates a hash based on the current state of this block
        :return:
        """
        block_string = json.dumps(self.as_dict(), sort_keys=True)
        return sha512(block_string.encode()).hexdigest()

    def as_dict(self) -> dict:
        """
        Returns this object but as a dictionary
        :return:
        """
        return self.__dict__
