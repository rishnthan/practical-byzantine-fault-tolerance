import aiohttp
from aiohttp import web
import sys
from PBFT import PBFTAggregator

class Node:

    def __init__(self, port, loop, corrupt=False):
        self.port = port
        self.loop = loop
        self.app = web.Application()
        self.app.add_routes([web.get('/status', self.status)])
        self.handler = self.app.make_handler()
        self.server = None
        self.corrupt = corrupt
        self.id = self.port - 8080

    async def status(self, request):
        return web.json_response(f'Node {self.id} Up and Running')

    def start(self):
        try:
            coroutine = self.loop.create_server(self.handler, '0.0.0.0', self.port)
            self.server = self.loop.run_until_complete(coroutine)
            address, port = self.server.sockets[0].getsockname()
            print(f'Node {self.id} started on http://{address}:{port}')
        except Exception as e:
            sys.stderr.write('Error: ' + format(str(e)) + "\n")
            sys.exit(1)

    def kill(self):
        self.server.close()
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.run_until_complete(self.handler.shutdown(60.0))
        self.loop.run_until_complete(self.app.cleanup())

class Commander(Node):
    async def receive():
        pass