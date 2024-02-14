import logging
import traceback
from typing import Optional, Awaitable

from tornado import concurrent
from tornado import web


class BaseHTTPHandler(web.RequestHandler):
    executor = concurrent.futures.ThreadPoolExecutor(5)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        print("setting headers for cors")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods',
                        ' PUT, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def post(self):
        pass

    def get(self):
        pass

    def get_argument_and_split(self, arg_name: str, delimiter: str = ','):
        arg_value = self.get_argument(arg_name, '')
        if arg_value == '':
            return []

        # make into lowercase
        arg_value = [s.lower() for s in arg_value.split(delimiter)]
        return arg_value

    @staticmethod
    def log_error(error_message, e):
        logging.error(f'{error_message}: {e}',
                      extra=dict(exception_detail=traceback.format_exc()))
