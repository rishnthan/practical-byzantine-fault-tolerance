import asyncio
from PBFT import PBFTAggregator

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

##########################################################################################################
    # Mutable variables - Can change this
    x = 5 # number of byzantine nodes
    type_of_byzantine = 0 # 0 - Offline Nodes, 1 - Malicious (Falsifying) Nodes
##########################################################################################################

    # Creates PBFTAggregator class object with x number of byzantine nodes
    pbft = PBFTAggregator(x, type_of_byzantine)

    # Generates class objects for each nodes
    # Note: Byzantine nodes are generated respective to their type
    pbft.createNodes(loop)
    pbft.startNodes()
    pbft.printNetworkInfo()
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
