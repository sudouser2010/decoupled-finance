import os
import asyncio
from typing import Optional, Awaitable

import tornado.web
from tornado import web, concurrent

PORT = 5000
UI_SETTINGS = {
    'path': os.path.abspath(os.path.join(os.path.dirname(__file__), 'webapp')),
    'default_filename': 'index.html'
}


class BaseHTTPHandler(web.RequestHandler):
    executor = concurrent.futures.ThreadPoolExecutor(5)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        print("setting headers for cors")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', ' PUT, DELETE, OPTIONS')


class HealthCheck(BaseHTTPHandler):
    def get(self):
        self.write({"status": "okay"})


def make_app():
    endpoints = [
        (r'/(.*)', tornado.web.StaticFileHandler, UI_SETTINGS),
    ]
    return tornado.web.Application(endpoints)


async def main():
    app = make_app()
    print('Running On Port:', PORT)
    app.listen(PORT)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
