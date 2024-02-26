import os
import asyncio
from typing import Optional, Awaitable

import tornado.web
from specific_import import import_file
from tornado import web, concurrent

CONSTANTS = import_file('../common/constants.py')

UI_SETTINGS = {
    'path': os.path.abspath(os.path.join(os.path.dirname(__file__), 'webapp')),
    'default_filename': 'index.html'
}

BLOCK_CHAIN_SERVER_URL = os.getenv(
    'BLOCK_CHAIN_SERVER_URL',
    CONSTANTS.DEVELOPMENT_BLOCK_CHAIN_URL
)


class BaseHTTPHandler(web.RequestHandler):
    executor = concurrent.futures.ThreadPoolExecutor(5)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        print("setting headers for cors")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', ' PUT, DELETE, OPTIONS')


class IndexHandler(BaseHTTPHandler):
    def get(self):
        self.render('index.html', BLOCK_CHAIN_SERVER_URL=BLOCK_CHAIN_SERVER_URL)


def make_app():
    endpoints = [
        (r'/', IndexHandler),
        (r'/index.html', IndexHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, UI_SETTINGS),
    ]
    return tornado.web.Application(endpoints, template_path=UI_SETTINGS['path'])


async def main():
    app = make_app()
    print('Running On Port:', CONSTANTS.WEBAPP_SERVER_PORT)
    app.listen(CONSTANTS.WEBAPP_SERVER_PORT)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
