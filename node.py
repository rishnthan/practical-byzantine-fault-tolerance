import aiohttp
from aiohttp import web
import sys
from datetime import datetime
from PBFT import PBFTAggregator

class Node:
    # initializing the node
    def __init__(self, port, loop, nodes_list, corrupt=False, commander=False):
        self.port = port
        self.loop = loop
        self.app = web.Application()
        self.app.add_routes([web.get('/status', self.status),
                             web.post('/preprepare', self.pre_prepare),
                             web.post('/prepare', self.prepare),
                             web.post('/commit', self.commit),
                             web.post('/reply', self.reply)])
        self.handler = self.app.make_handler()
        self.server = None
        self.corrupt = corrupt
        self.commander = commander
        self.id = self.port - 8080
        self.nodes_list = nodes_list
        self.session = aiohttp.ClientSession()

    # Handler for status router
    async def status(self, request):
        return web.json_response(f'Node {self.id} Up and Running')

    # First stage of PBFT - Pre-Prepare
    async def pre_prepare(self, request):
        # Only commanders can initiate PBFT from client's request
        if self.commander:
            message = await request.json()
            # Checking execution time
            start_time = datetime.now()
            # Sending client's message to all the nodes which initiates the pre-prepare stage
            for i in self.nodes_list:
                if self.id != i:
                    async with self.session.post(f'http://localhost:{8080 + i}/prepare', json=message) as response:
                        pass
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            print(f"\n\nPBFT Consensus Time: {execution_time}")
            PBFTAggregator.checkReplies()
            return web.Response(text=f'\nPBFT Consensus Time: {execution_time}s\n')
        else:
            return web.HTTPUnauthorized()

    # Second stage of PBFT - Prepare
    async def prepare(self, request):
        message = await request.json()
        # For type_of_byzantine = 1 (Malicious (Falsifying) Nodes)
        # Corrupts the message received from Commander Node
        if self.corrupt:
            message["data"] = "Corrupt"
        # Sending received message from Commander Node to all the other nodes which initiates the prepare stage
        for i in self.nodes_list:
                if self.id != i:
                    await self.session.post(f'http://localhost:{8080 + i}/commit', json=message)
        return web.HTTPOk()
    
    # Third stage of PBFT - Commit
    async def commit(self, request):
        message = await request.json()
        # For type_of_byzantine = 1 (Malicious (Falsifying) Nodes)
        # Corrupts the message only if the node is a commander node and corrupt
        if self.corrupt and self.commander:
            message["data"] = "Corrupt"
        # Sending prepare message from all other nodes to all the other nodes which initiates the commit stage
        for i in self.nodes_list:
                if self.id != i:
                    await self.session.post(f'http://localhost:{8080 + i}/reply', json=message)
        return web.HTTPOk()
    
    # Final stage of PBFT - Reply
    async def reply(self, request):
        message = await request.json()
        # Receiving commit message from all other nodes
        # Sending the message to Client
        PBFTAggregator.receiveReplies([self.id, message["data"]]) # Simulating sending reply to client
        return web.HTTPOk()

    # Starting the Node
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

    # Killing the Node
    def kill(self):
        # await self.session.close()
        self.server.close()
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.run_until_complete(self.handler.shutdown(60.0))
        self.loop.run_until_complete(self.app.cleanup())
