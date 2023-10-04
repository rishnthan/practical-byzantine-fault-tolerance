import asyncio
import node
from PBFT import PBFTAggregator

if __name__ == '__main__':
    # loop = asyncio.get_event_loop() (for python 3.10 and below)
    loop = asyncio.new_event_loop() # (for python 3.11 and above)
    asyncio.set_event_loop(loop)
    x = 1 # n in 3n+1
    pbft = PBFTAggregator(x)

    total_nodes = pbft.getNodes()
    byzantine_nodes = pbft.getByzantineNodes()
    commander_nodes = pbft.getCommanderNode()
    nodes = []
    # 0 - Offline Nodes, 1 - Malicious (Falsifying) Nodes
    type_of_byzantine = 1

    print(f"Total Nodes: {len(total_nodes)} -> {total_nodes}")
    print(f"Byzantine Nodes: {len(byzantine_nodes) if type_of_byzantine == 1 else 0}  -> {byzantine_nodes if type_of_byzantine == 1 else '[NULL]'}")
    print(f"Commander Node: {len(commander_nodes)} -> {commander_nodes}")

    if type_of_byzantine == 0: # Offline Nodes
        for i in total_nodes:
            if int(i) in commander_nodes:
                nodes.append(node.Node(8080 + i, loop, total_nodes, False, True))
            else:
                nodes.append(node.Node(8080 + i, loop, total_nodes))
    else: # Malicious (Falsifying) Nodes
        for i in total_nodes:
            if int(i) in commander_nodes:
                nodes.append(node.Node(8080 + i, loop, total_nodes, True if int(i) in byzantine_nodes else False, True))
            elif int(i) in byzantine_nodes:
                nodes.append(node.Node(8080 + i, loop, total_nodes, True))
            else:
                nodes.append(node.Node(8080 + i, loop, total_nodes))

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