"""
This is a webserver which does the following:
    -starts a Decoupled blockchain instance
    -returns the latest unmined block
    -mines an unmined block with a given proof

    Todo:
        -records transactions in current block
        -returns transactions in any previous block
"""
import asyncio

from specific_import import import_file
import tornado.web
from tornado import gen


BaseHTTPHandler = import_file('base_http_handler.py').BaseHTTPHandler
Blockchain = import_file('../common/blockchain/blockchain.py').Blockchain
CONSTANTS = import_file('../common/constants.py')

# initialize and run blockchain
BLOCKCHAIN = Blockchain()
BLOCKCHAIN.run()


class HealthCheck(BaseHTTPHandler):
    def get(self):
        self.write({"status": "okay"})


class Transaction(BaseHTTPHandler):
    @tornado.gen.coroutine
    def post(self):
        """
        records a valid transaction to current block
        :return:
        """
        pass

    def get(self):
        """
        returns transactions in a given block
        :return:
        """


class UnminedBlock(BaseHTTPHandler):
    @tornado.gen.coroutine
    def post(self):
        """
        Uses proof to solve the unmined block.
        :return:
        """
        try:
            proof: str = self.get_argument_and_split('proof')
            account: str = self.get_argument_and_split('account')
            success = BLOCKCHAIN.mine_block(account, proof)
            amount_mined = 0

            if success:
                amount_mined = BLOCKCHAIN.amount_mined_per_block()

            result = {
                'data': {
                    'success': success,
                    'account': account,
                    'amount_mined': amount_mined
                }
            }
            self.write(result)

        except (Exception,) as e:
            self.set_status(500)
            self.write('ERROR MINING WITH PROOF')

    def get(self):
        """
        Gets the current the unmined block
        :return:
        """
        try:
            unmined_block = BLOCKCHAIN.unmined_block
            if unmined_block:
                data = unmined_block.as_dict()
            else:
                data = None

            self.write({
                'data': data
            })

        except (Exception,) as e:
            self.set_status(500)
            self.write('ERROR GETTING UNMINED BLOCK')


def make_app():
    endpoints = [
        # (r'/transaction', Transaction),
        (r'/unmined-block', UnminedBlock),
        (r'/health-check', HealthCheck),
    ]
    return tornado.web.Application(endpoints)


async def main():
    app = make_app()
    print('Running On Port:', CONSTANTS.PORT)
    app.listen(CONSTANTS.PORT)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
