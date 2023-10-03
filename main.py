import asyncio
from node import Node


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    node = []
    for i in range(4):
        node.append(Node(i, 8080 + i, loop))
        node[i].start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for i in range(4):
            node[i].kill()
        loop.close()