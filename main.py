import asyncio
import node
from PBFT import PBFTAggregator

if __name__ == '__main__':

    x = 70 # n in 3n+1
    pbft = PBFTAggregator(x)

    total_nodes = pbft.getNodes()
    byzantine_nodes = pbft.getByzantineNodes()
    commander_node = pbft.getCommanderNode()
    nodes = []


    print(f"Total Nodes: {len(total_nodes)} -> {total_nodes}")
    print(f"Byzantine Nodes: {len(byzantine_nodes)} -> {byzantine_nodes}")
    print(f"Commander Node: {commander_node}")


    loop = asyncio.get_event_loop()

    for i in total_nodes:
        if int(i) == commander_node:
            nodes.append(node.Commander(8080 + i, loop, True if int(i) in byzantine_nodes else False))
        elif int(i) in byzantine_nodes:
            nodes.append(node.Node(8080 + i, loop, True))
        else:
            nodes.append(node.Node(8080 + i, loop))

    print("\n Starting Nodes \n")

    for node in nodes:
        node.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for node in nodes:
            node.kill()
        loop.close()