import asyncio
from PBFT import PBFTAggregator
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

##########################################################################################################
    # Mutable variables - Can change this
    x = 10000 # number of byzantine nodes
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

    #print(f"\n{pbft.getCoordinates()}")
    #for i in pbft.getClusterDistances():
        #print(i)
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