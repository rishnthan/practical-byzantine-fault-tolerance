from aiohttp import web
import asyncio
import sys


class Node:

    def __init__(self, port, loop):
        self.port = port
        self.loop = loop
        self.app = web.Application()
        self.app.router.add_get('/status', self.handle)
        self.handler = web.AppRunner(self.app)
        self.server = None
        

    async def handle(request):
        return web.json_response(f'App OK')
    
    def start(self):
        try:
            coroutine = self.loop.create_server(self.handler, '0.0.0.0', self.port)
            self.server = self.loop.run_until_complete(coroutine)
            address, port = self.server.sockets[0].getsockname()
            print(f'App started on http://{address}:{port}')
        except Exception as e:
            sys.stderr.write('Error: ' + format(str(e)) + "\n")
            sys.exit(1)

    def kill(self):
        self.server.close()
        self.loop.run_until_complete(self.app.shutdown())
        self.loop.run_until_complete(self.handler.shutdown(60.0))
        self.loop.run_until_complete(self.handler.finish_connections(1.0))
        self.loop.run_until_complete(self.app.cleanup())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    node0 = Node(8080, loop)
    node1 = Node(8081, loop)

    node0.start()
    node1.start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        node0.kill()
        node1.kill()
        loop.close()