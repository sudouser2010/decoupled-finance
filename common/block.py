import copy
from dataclasses import dataclass
from hashlib import sha512
import json


@dataclass
class BlockMetaData:
    has_been_mined: bool = False


class Block:

    def __init__(self, index: int, transactions: list[dict],
                 end_timestamp: int, previous_hash: str, difficulty: int = 1):
        # used for determining order in blockchain
        self.index = index

        # used for finding a proof for block
        self.nonce = 0

        self.transactions = transactions
        self.end_timestamp = end_timestamp
        self.previous_hash = previous_hash

        self.hash = ''
        self.difficulty = difficulty

        # __meta__ stores meta data on the block
        self.__meta__ = BlockMetaData()

    def compute_hash(self, nonce: int) -> str:
        """
        Creates a hash based on the
            current state of the block
            and the nonce value
        :return:
        """
        # set block nonce before getting hash
        block_dict = self.as_dict()
        block_dict['nonce'] = nonce

        block_string = json.dumps(block_dict, sort_keys=True)
        block_hash = sha512(block_string.encode()).hexdigest()

        return block_hash

    def as_dict(self) -> dict:
        """
        Returns this object but as a dictionary
        :return:
        """
        d = copy.deepcopy(self.__dict__)

        # remove block meta data
        del d['__meta__']

        return d
