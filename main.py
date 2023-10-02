from aiohttp import web
import asyncio
import sys

async def status1(request):
    return web.json_response('App1 OK')

async def status2(request):
    return web.json_response('App2 OK')

def start():
    try:
        loop = asyncio.get_event_loop()

        # App1
        app1 = web.Application()
        app1.router.add_get('/status', status1)
        handler1 = web.AppRunner(app1)
        coroutine1 = loop.create_server(handler1, '0.0.0.0', 8081)
        server1 = loop.run_until_complete(coroutine1)
        address1, port1 = server1.sockets[0].getsockname()
        print('App1 started on http://{}:{}'.format(address1, port1))

        # App2
        app2 = web.Application()
        app2.router.add_get('/status', status2)
        handler2 = web.AppRunner(app2)
        coroutine2 = loop.create_server(handler2, '0.0.0.0', 8082)
        server2 = loop.run_until_complete(coroutine2)
        address2, port2 = server2.sockets[0].getsockname()
        print('App2 started on http://{}:{}'.format(address2, port2))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server1.close()
            loop.run_until_complete(app1.shutdown())
            loop.run_until_complete(handler1.shutdown(60.0))
            loop.run_until_complete(handler1.finish_connections(1.0))
            loop.run_until_complete(app1.cleanup())

            server2.close()
            loop.run_until_complete(app2.shutdown())
            loop.run_until_complete(handler2.shutdown(60.0))
            loop.run_until_complete(handler2.finish_connections(1.0))
            loop.run_until_complete(app2.cleanup())

        loop.close()
    except Exception as e:
        sys.stderr.write('Error: ' + format(str(e)) + "\n")
        sys.exit(1)

if __name__ == '__main__':
    start()
from aiohttp import web
import asyncio
import sys


class Node:

    def __init__(self, port):
        self.port = port

    async def status(request):
        return web.json_response(f'App on {self.port} OK')
    
    def start(self):
        try:
            loop = asyncio.get_event_loop()

            app = web.Application()
            app.router.add_get('/status', self.status)
            handler = web.AppRunner(app)
            coroutine = loop.create_server(handler, 'localhost', self.port)
            server = loop.run_until_complete(coroutine)
            address, port = server.sockets[0].getsockname()
            print(f'App started on http://{address}:{port}')
        except Exception as e:
            sys.stderr.write('Error: ' + format(str(e)) + "\n")
            sys.exit(1)


if __name__ == '__main__':
    Node(8081).start()
    Node(8082).start()