import time
from threading import Thread

from tinydb import TinyDB, Query
from specific_import import import_file

table_get = import_file('../table_utils.py').table_get
Block = import_file('../block.py').Block
Transaction = import_file('../transaction.py').Transaction
BLOCK_DB_LOCATION = import_file('../constants.py').BLOCK_DB_LOCATION
STATE_DB_LOCATION = import_file('../constants.py').STATE_DB_LOCATION

block_db = TinyDB(BLOCK_DB_LOCATION)
state_db = TinyDB(STATE_DB_LOCATION)


class Blockchain:
    """
    This keeps track of the:
        * blockchain history
        * token amounts
        * unmined block data
    """

    def __init__(self, seconds_between_blocks: int = 60):
        # set persistent blockchain attributes
        self.seconds_between_blocks = seconds_between_blocks
        self.difficulty: int = 1
        self.block_table = block_db.table('block')
        self.amount_table = state_db.table('amount')
        self.active = True

        # for blockchain history
        self.chain: list[Block] = []

        # for unmined block data
        self.index: int = 0
        self.unmined_transactions: list[dict] = []
        self.unmined_timestamp: int = self.int_timestamp()
        self.unmined_block = None

        # create first block
        self.create_first_block()

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
        return int(time.time())

    @property
    def previous_block(self) -> Block:
        return self.chain[-1]

    def reset_unmined_block_data(self):
        self.index += 1
        self.unmined_timestamp += self.seconds_between_blocks
        self.unmined_block = None

    def create_first_block(self):
        genesis_block = Block(
            index=0,
            transactions=[],
            end_timestamp=self.int_timestamp(),
            previous_hash=None,
            difficulty=self.difficulty
        )
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        self.reset_unmined_block_data()

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
            previous_hash=self.previous_block.hash,
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

    def increase_address_amount_after_mining(self, address: str):
        default_account = {'address': address, 'amount': 0}
        query = Query().address == address

        account_state = table_get(self.amount_table, query, default_account)

        account_state['amount'] += self.amount_mined_per_block
        self.amount_table.upsert(account_state, query)

    def mine_block(self, address: str, proof: str) -> bool:
        """
        :param address: a hash representing the miner's account
        :param proof: a hash which makes the unmined_block valid
        :return:
        """
        # when an unmined block does not exist, return False
        if self.unmined_block is None:
            return False

        # when proof for the unmined block does not work, return False
        if not self.is_valid_proof(self.unmined_block, proof):
            return False

        self.unmined_block.hash = proof
        self.update_blockchain_data(self.unmined_block)
        self.reset_unmined_block_data()
        self.increase_address_amount_after_mining(address)
        return True

    def is_valid_proof(self, block: Block, block_hash: str):
        return (block_hash.startswith('0' * self.difficulty)
                and block_hash == block.compute_hash())

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

    def run_blocking(self):
        while self.active:
            self.delay_loop()

            unmined_block_has_not_ended = self.int_timestamp(
            ) < self.unmined_timestamp
            unmined_block_has_not_been_mined = self.unmined_block is not None
            """
            if the unmined block is still open for storing transactions, then don't set the unmined_block.
                Also...
            if the unmined block already exists, then it hasn't been mined and we shouldn't set another unmined_block
                b/c doing so would discard the preexisting unmined_block.
                This works b/c when an unmined_block is mined, then it is set to None
            """
            if unmined_block_has_not_ended or unmined_block_has_not_been_mined:
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
