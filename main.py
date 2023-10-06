import asyncio
import node
from PBFT import PBFTAggregator

if __name__ == '__main__':
    # loop = asyncio.get_event_loop() (for python 3.10 and below)
    loop = asyncio.new_event_loop() # (for python 3.11 and above)
    asyncio.set_event_loop(loop)

##########################################################################################################
    # Mutable variables - Can change this
    x = 100 # number of byzantine nodes
    type_of_byzantine = 0 # 0 - Offline Nodes, 1 - Malicious (Falsifying) Nodes
##########################################################################################################

    # Creates PBFTAggregator class object with x number of byzantine nodes
    pbft = PBFTAggregator(x)

    # Gets a list of the total nodes that will be deployed to the network
    total_nodes = pbft.getNodes()
    # Gets a list of the nodes that are byzantine
    byzantine_nodes = pbft.getByzantineNodes()
    # Gets a list of the commander nodes (For now only 1, can add manually in PBFT code)
    commander_nodes = pbft.getCommanderNode()

    # Empty List to store the nodes' aiohttp web server instance
    nodes = []

    # Prints information about the nodes in network
    print(f"Total Nodes: {len(total_nodes)} -> {total_nodes if len(total_nodes) < 10 else ''}")
    print(f"Byzantine Nodes: {len(byzantine_nodes)}  -> {byzantine_nodes if len(byzantine_nodes) < 10 else ''}")
    print(f"Commander Node: {len(commander_nodes)} -> {commander_nodes}")

    # Generates class objects for each nodes
    # Note: Byzantine nodes are generated respective to their type
    if type_of_byzantine == 0: # Offline Nodes
        for i in total_nodes:
            # Checks if node is commander node
            if int(i) in commander_nodes:
                # Generates commander node class object
                # Note: for offline byzantine type, commander node can never be 
                # byzantine else PBFT won't be initiated
                nodes.append(node.Node(8080 + i, loop, total_nodes, False, True))
            # Checks if node is a byzantine node
            elif int(i) in byzantine_nodes:
                # Forgo creating byzantine nodes class object
                # to simulate offline byzantine nodes
                pass
            else:
                # Generates the rest of the nodes class object while ignoring byzantine
                nodes.append(node.Node(8080 + i, loop, total_nodes))
    else: # Malicious (Falsifying) Nodes
        for i in total_nodes:
            # Checks if node is a commander node
            if int(i) in commander_nodes:
                # Generates commander node class object
                nodes.append(node.Node(8080 + i, loop, total_nodes, True if int(i) in byzantine_nodes else False, True))
            # Checks if node is a byzantine node
            elif int(i) in byzantine_nodes:
                # Generates byzantine node class object to later falsify the data
                nodes.append(node.Node(8080 + i, loop, total_nodes, True))
            else:
                # Generates the rest of the nodes' class objects
                nodes.append(node.Node(8080 + i, loop, total_nodes))

    # Starts the nodes' webservers
    print("\n Starting Nodes \n")
    for node in nodes:
        node.start()
    
    print(f"\nNode {int(commander_nodes[0])} is the commander node.\n" 
          f"Running on http://0.0.0.0:{8080 + int(commander_nodes[0])}")
    # initializes the replies list to collect the replies of the nodes from PBFT
    # once nodes are created and started.
    PBFTAggregator.initReplies(len(total_nodes))

    # Ensures the webservers runs forever
    try:
        loop.run_forever()
    # If KeyboardInterrupt is called, it will kill the nodes in the server and 
    # stops the asyncio loop
    except KeyboardInterrupt:
        pass
    finally:
        # Kills the nodes' webservers
        for node in nodes:
            node.kill()
        loop.close()