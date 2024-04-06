"""
This is Python-based code that will do mining
"""
import json
import time
from hashlib import sha512

import requests
from specific_import import import_file

CONSTANTS = import_file('../common/constants.py')


class Mine:
    def __init__(self, address_doing_mining: str, master_node_url: str, port: int, seconds_between_attempts=.5):
        self.address_doing_mining = address_doing_mining
        self.seconds_between_attempts = seconds_between_attempts
        self.url = f'{master_node_url}:{port}/unmined-block'

    @staticmethod
    def find_winning_nonce(unmined_block: dict) -> int:
        """
        Loops through repeatedly and finds the nonce which results in a valid block hash.
        Each loop the block nonce is incremented
        :return:
        """
        difficulty = unmined_block['difficulty']

        while True:
            block_string = json.dumps(unmined_block, sort_keys=True)
            block_hash = sha512(block_string.encode()).hexdigest()
            block_hash_is_valid = block_hash.startswith('0' * difficulty)
            print(block_hash)
            if block_hash_is_valid:
                return unmined_block['nonce']

            # when hash doesn't meet condition, adjust the nonce and try again
            unmined_block['nonce'] += 1

    def run(self):
        while True:
            try:
                time.sleep(self.seconds_between_attempts)
                r = requests.get(url=self.url)
                data = r.json()
                unmined_block = data.get('data')

                if not unmined_block:
                    continue

                winning_nonce = self.find_winning_nonce(unmined_block)

                data = {
                    'winning_nonce': winning_nonce,
                    'address': self.address_doing_mining
                }
                r = requests.post(url=self.url, data=data)
                data = r.json()
                mining_result = data.get('data')

                print('RESULT', mining_result)
            except Exception as e:
                print('Error Mining', e)


if __name__ == '__main__':
    m = Mine(
        address_doing_mining='placeholder',
        master_node_url='http://localhost',
        port=CONSTANTS.BLOCK_CHAIN_SERVER_PORT
    )
    m.run()
