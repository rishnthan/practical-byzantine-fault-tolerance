import aiohttp
from aiohttp import web
import sys
from datetime import datetime
from PBFT import PBFTAggregator

class Node:

    def __init__(self, port, loop, nodes_list, corrupt=False, commander=False):
        self.port = port
        self.loop = loop
        self.app = web.Application()
        self.app.add_routes([web.get('/status', self.status),
                             web.post('/receive', self.receive),
                             web.post('/preprepare', self.pre_prepare),
                             web.post('/prepare', self.prepare),
                             web.post('/commit', self.commit)])
        self.handler = self.app.make_handler()
        self.server = None
        self.corrupt = corrupt
        self.commander = commander
        self.id = self.port - 8080
        self.nodes_list = nodes_list
        self.session = aiohttp.ClientSession()

    async def status(self, request):
        return web.json_response(f'Node {self.id} Up and Running')

    async def receive(self, request):
        if self.commander:
            message = await request.json()
            start_time = datetime.now()
            for i in self.nodes_list:
                if self.id != i:
                    async with self.session.post(f'http://localhost:{8080 + i}/preprepare', json=message) as response:
                        pass
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            print(f"\n\nPBFT Consensus Time: {execution_time}")
            PBFTAggregator.checkReplies()
            return web.Response(text=f'\nPBFT Consensus Time: {execution_time}s\n')
        else:
            return web.HTTPUnauthorized()

    async def pre_prepare(self, request):
        message = await request.json()
        if self.corrupt:
            message["data"] = "Corrupt"
        for i in self.nodes_list:
                if self.id != i:
                    await self.session.post(f'http://localhost:{8080 + i}/prepare', json=message)
        return web.HTTPOk()
    
    async def prepare(self, request):
        message = await request.json()
        if self.corrupt and self.commander:
            message["data"] = "Corrupt"
        for i in self.nodes_list:
                if self.id != i:
                    await self.session.post(f'http://localhost:{8080 + i}/commit', json=message)
        return web.HTTPOk()
    
    async def commit(self, request):
        message = await request.json()
        PBFTAggregator.receiveReplies([self.id, message["data"]])
        return web.HTTPOk()

    def start(self):
        try:
            coroutine = self.loop.create_server(
                self.handler, '0.0.0.0', self.port)
            self.server = self.loop.run_until_complete(coroutine)
            address, port = self.server.sockets[0].getsockname()
            print(f'Node {self.id} started on http://{address}:{port}')
        except Exception as e:
            sys.stderr.write('Error: ' + format(str(e)) + "\n")
            sys.exit(1)

    def kill(self):
        # await self.session.close()
        self.server.close()
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.run_until_complete(self.handler.shutdown(60.0))
        self.loop.run_until_complete(self.app.cleanup())
