import math
import time
from threading import Thread

from tinydb import TinyDB, Query
from specific_import import import_file

table_get = import_file('../table_utils.py').table_get
Block = import_file('../block.py').Block
Transaction = import_file('../transaction.py').Transaction
BLOCK_DB_LOCATION = import_file('../constants.py').BLOCK_DB_LOCATION
STATE_DB_LOCATION = import_file('../constants.py').STATE_DB_LOCATION
BLOCK_DURATION_IN_SECONDS_LOWER_LIMIT = import_file('../constants.py').BLOCK_DURATION_IN_SECONDS_LOWER_LIMIT
LOAD_FROM_DB_ON_RESTART = import_file('../constants.py').LOAD_FROM_DB_ON_RESTART

block_db = TinyDB(BLOCK_DB_LOCATION)
state_db = TinyDB(STATE_DB_LOCATION)


class Blockchain:
    """
    This keeps track of the:
        * blockchain history
        * token amounts
        * unmined block data
    """

    def __init__(self):
        # set persistent blockchain attributes
        self.seconds_between_blocks = BLOCK_DURATION_IN_SECONDS_LOWER_LIMIT
        self.difficulty: int = 1
        self.block_table = block_db.table('block')
        self.amount_table = state_db.table('amount')
        self.active = True

        # for unmined block data
        self.index: int = 0
        self.unmined_transactions: list[dict] = []
        self.unmined_timestamp: int = self.int_timestamp() + self.seconds_between_blocks
        self.unmined_block = None

        # for blockchain history
        self.chain: list[Block] = []
        self.setup_blockchain_data()

        # initialize first block
        self.set_unmined_block()

    def setup_blockchain_data(self):
        if LOAD_FROM_DB_ON_RESTART:
            # load block_chain data
            self.chain = [
                dict(entry) for entry in self.block_table.all()
            ]
        else:
            # clear block_chain and amount tables
            self.block_table.truncate()
            self.amount_table.truncate()

        self.index = len(self.chain)

    def load_preexisting_blockchain_data_from_db(self):
        pass

    @property
    def amount_mined_per_block(self):
        """
        todo: make the amount returned per block decrease as the block index increases.
        :return:
        """
        return 1

    @staticmethod
    def int_timestamp() -> int:
        """
        Returns the seconds since the epoch as an int
        :return:
        """
        return math.floor(time.time())

    def reset_unmined_block_data(self):
        self.index += 1
        self.unmined_timestamp += self.seconds_between_blocks

    def set_unmined_block(self) -> None:
        """
        :return:
        """
        # store a snapshot of the unmined_transactions
        unmined_transactions_copy = self.unmined_transactions[::]

        self.unmined_block = Block(
            index=self.index,
            transactions=unmined_transactions_copy,
            end_timestamp=self.unmined_timestamp,
            previous_hash=None,
            difficulty=self.difficulty
        )
        """
            reset unmined_transaction so that any transactions
            submitted after will go into the next unmined_block
        """
        self.unmined_transactions = []

    def update_blockchain_data(self, new_block: Block):
        new_block = new_block.as_dict()

        # update non-persistent blockchain data
        self.chain.append(new_block)

        # update persistent blockchain data
        self.block_table.insert(new_block)

    def get_address_state(self, address: str):
        default_state = {'address': address, 'amount': 0}
        query = Query().address == address
        state = table_get(self.amount_table, query, default_state)
        return state

    def increase_address_amount_after_mining(self, address: str):
        default_account = {'address': address, 'amount': 0}
        query = Query().address == address

        account_state = table_get(self.amount_table, query, default_account)

        account_state['amount'] += self.amount_mined_per_block
        self.amount_table.upsert(account_state, query)

    def mine_block(self, address: str, winning_nonce: int) -> bool:
        """
        :param address: a hash representing the miner's account
        :param winning_nonce: a nonce which makes the hash of the unmined_block valid
        :return:
        """
        if not self.unmined_block_has_ended:
            return False

        # compute hash based on wining_nonce
        block_hash = self.unmined_block.compute_hash(winning_nonce)
        difficulty = self.unmined_block.difficulty

        # when nonce for the unmined block does not work, return False
        if not self.is_hash_valid(block_hash, difficulty):
            return False

        self.unmined_block.hash = block_hash
        self.unmined_block.nonce = winning_nonce
        self.unmined_block.__meta__.has_been_mined = True

        if len(self.chain):
            self.unmined_block.previous_hash = self.chain[-1]['hash']

        self.update_blockchain_data(self.unmined_block)
        self.reset_unmined_block_data()
        self.increase_address_amount_after_mining(address)
        return True

    @staticmethod
    def is_hash_valid(block_hash: str, difficulty: int):
        """
        block_hash is considered valid when it starts with zero

        :param block_hash:
        :param difficulty:
        :return:
        """
        return block_hash.startswith('0' * difficulty)

    def add_unmined_transaction(self, transaction: Transaction):
        """.
        Appends to unmined_transactions.
        Useful when adding a transaction to current unmined_block.

        :param transaction:
        :return:
        """
        self.unmined_transactions.append(transaction.as_dict())

    def add_unmined_transactions(self, transactions: list[dict]):
        """.
        Extends unmined_transactions.
        Useful when adding transactions that didn't
        make it into the previous closed block.

        :param transactions:
        :return:
        """
        self.unmined_transactions.extend(transactions)

    @staticmethod
    def delay_loop(delay: float = .1):
        """
        This is used to slow execution of while loop
        :param delay:
        :return:
        """
        time.sleep(delay)

    @property
    def unmined_block_has_ended(self) -> bool:
        return self.int_timestamp() > self.unmined_timestamp

    def run_blocking(self):
        while self.active:
            self.delay_loop()

            # if the unmined block is still open for storing transactions, then don't set the unmined_block.
            if not self.unmined_block_has_ended:
                continue

            """
            if the unmined block already exists, then it hasn't been mined and we shouldn't set another unmined_block
                b/c doing so would discard the preexisting unmined_block.
                This works b/c when an unmined_block is mined, then it is set to None
            """
            if not self.unmined_block.__meta__.has_been_mined:
                continue

            """
            create an unmined block based on the previous block and
            a snapshot of current unmined transactions
            """
            self.set_unmined_block()

    def run(self):
        """
        runs the blocking part of code in its own thread
        :return:
        """
        th = Thread(target=self.run_blocking, )
        th.start()
