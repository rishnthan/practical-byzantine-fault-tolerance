import asyncio
from PBFT import PBFTAggregator

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

##########################################################################################################
    # Mutable variables - Can change this
    x = 2 # number of byzantine nodes
    type_of_byzantine = 1 # 0 - Offline Nodes, 1 - Malicious (Falsifying) Nodes
##########################################################################################################

    # Creates PBFTAggregator class object with x number of byzantine nodes
    pbft = PBFTAggregator(x, type_of_byzantine)

    # Generates class objects for each nodes
    # Note: Byzantine nodes are generated respective to their type
    pbft.createNodes(loop)
    pbft.startNodes()
    pbft.printNetworkInfo()

    PBFTAggregator.initReplies(len(pbft.getNodes()))
    PBFTAggregator.initClusterList(pbft.getClusters())

    # Ensures the webservers runs forever
    try:
        loop.run_forever()
    # If KeyboardInterrupt is called, it will kill the nodes in the server and 
    # stops the asyncio loop
    except KeyboardInterrupt:
        pass
    finally:
        # Kills the nodes' webservers
        pbft.killNodes()
        loop.close()

"""
Total Nodes: 16
No. of Clusters: 4
Commanders: [7, 1, 3, 6]
Byzantine Nodes: [8, 9, 10, 12]
Clusters: [[0, 5, 7, 12], [1, 8, 9, 14], [2, 3, 10, 15], [4, 6, 11, 13]]
Node 0 -> 3 Correct 0 Corrupt
Node 1 -> 0 Correct 0 Corrupt
Node 2 -> 3 Correct 0 Corrupt
Node 3 -> 2 Correct 0 Corrupt
Node 4 -> 7 Correct 0 Corrupt
Node 5 -> 3 Correct 0 Corrupt
Node 6 -> 6 Correct 0 Corrupt
Node 7 -> 2 Correct 0 Corrupt
                                    Node 8 -> 0 Correct 0 Corrupt
                                    Node 9 -> 0 Correct 0 Corrupt
                                    Node 10 -> 0 Correct 0 Corrupt
Node 11 -> 7 Correct 0 Corrupt
                                    Node 12 -> 0 Correct 0 Corrupt
Node 13 -> 7 Correct 0 Corrupt
Node 14 -> 1 Correct 0 Corrupt
Node 15 -> 3 Correct 0 Corrupt
"""