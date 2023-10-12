import random
import node

# dictionary to collect replies of nodes after final stage of PBFT
replies_list = {}
clusters_list = []

# PBFT Aggregator Class
class PBFTAggregator:
    # Initiate the class
    def __init__(self, num_of_byzantine, type_of_byzantine):
        self.__num_of_byzantines = num_of_byzantine
        self.__type_of_byzantine = type_of_byzantine
        self.__node_objects = []
        self.__nodes_list = self.__nodes_list()
        self.__clusters = self.__cluster_nodes()
        self.__commander_nodes = self.__gen_commander_nodes()
        self.__byzantine_nodes = self.__gen_byzantine_nodes()

    # Generate node list
    def __nodes_list(self):
        nodes_list = []
        total_nodes = 3*self.__num_of_byzantines+1
        if total_nodes % 4 != 0:
            total_nodes += 4 - total_nodes % 4
        for i in range(0, total_nodes):
            nodes_list.append(i)
        return nodes_list

    def __cluster_nodes(self):
        temp_list = list(self.__nodes_list)
        cluster_nodes_list = []
        for i in range(len(self.__nodes_list)//4):
            cluster = []
            for j in range(4):
                x = random.choice(temp_list)
                cluster.append(x)
                temp_list.remove(x)
            cluster.sort()
            cluster_nodes_list.append(cluster)
        cluster_nodes_list.sort()
        return cluster_nodes_list

    # Select Commander Node at random
    def __gen_commander_nodes(self):
        commander_nodes_list = []
        for i in self.__clusters:
            x = random.choice(i)
            commander_nodes_list.append(x)
        return commander_nodes_list

    # Select Byzantine Nodes at random
    def __gen_byzantine_nodes(self):
        temp_list = list(self.__nodes_list)
        byzantine_nodes = []
        if self.__type_of_byzantine == 0:
            for i in temp_list:
                if i in self.__commander_nodes:
                    temp_list.remove(i)
        for i in range(self.__num_of_byzantines):
            x = random.choice(temp_list)
            temp_list.remove(x)
            byzantine_nodes.append(x)
        byzantine_nodes.sort()
        return byzantine_nodes
            

    # Get nodes_list from class instance
    def getNodes(self):
        return self.__nodes_list

    def getClusters(self):
        return self.__clusters

    # Get byzantine_nodes from class instance
    def getByzantineNodes(self):
        return self.__byzantine_nodes

    # Get commander_node from class instance
    def getCommanderNodes(self):
        return self.__commander_nodes

    def getCommanderCluster(self, commanderNode):
        for i in self.__clusters:
            if commanderNode in i:
                return i
            
    def printNetworkInfo(self):
        print("Network Information")
        print("-------------------")
        print(f"Total Nodes: {len(self.__nodes_list)}")
        print(f"No. of Clusters: {len(self.__clusters)}")
        print(f"Commanders: {len(self.__commander_nodes)}")
        print(f"Byzantine Nodes: {len(self.__byzantine_nodes)}")
        if len(self.__clusters) < 5:
            print(f"Clusters: {self.__clusters}")
        temp_list = list(self.__commander_nodes)
        temp_list.sort()
        print(f"\n\nSend Request to http://localhost:{8080 + temp_list[0]}/request ")
              
            
    def createNodes(self, loop):
        for cluster in self.__clusters:
            for i in cluster:
                if self.__type_of_byzantine == 0:
                    if i in self.__commander_nodes:
                        commander = node.Node(8080 + i, loop, cluster, False, True, self.__commander_nodes)
                        self.__node_objects.append(commander)
                    elif i in self.__byzantine_nodes:
                        # print(f"Node {i} started on http://0.0.0.0:{8080 + i}")
                        pass
                    else:
                        rest = node.Node(8080 + i, loop, cluster)
                        self.__node_objects.append(rest)
                else:
                    if i in self.__commander_nodes:
                        commander = node.Node(8080 + i, loop, cluster, True if node in self.__byzantine_nodes else False, True, self.__commander_nodes)
                        self.__node_objects.append(commander)
                    elif i in self.__byzantine_nodes:
                        byzantine = node.Node(8080 + i, loop, cluster, True)
                        self.__node_objects.append(byzantine)
                    else:
                        rest = node.Node(8080 + i, loop, cluster)
                        self.__node_objects.append(rest)
    
    def startNodes(self):
        for node in self.__node_objects:
            node.start()

    def killNodes(self):
        for node in self.__node_objects:
            node.kill()

    # Initializes replies_list dictionary
    @staticmethod
    def initReplies(total_nodes):
        for i in range(total_nodes):
            replies_list[i] = []
        
    @staticmethod
    def initClusterList(clusters):
        for i in clusters:
            clusters_list.append(i)

    # Receives data from nodes @ reply stage
    @staticmethod
    def receiveReplies(data):
        replies_list[data[0]].append(data[1])

    # Resets replies_list for next consensus run
    @staticmethod
    def resetReplies(total_nodes):
        replies_list.clear()
        PBFTAggregator.initReplies(total_nodes)

    # Counts and display node's data and number of corrupted, correct entries
    @staticmethod
    def checkReplies(execution_time):
        num_of_corrupt = 0
        num_of_correct = 0
        for key, value in replies_list.items():
            num_of_corrupt += value.count("Corrupt")
            num_of_correct += len(replies_list[key]) - value.count("Corrupt")

        if num_of_correct > num_of_corrupt:
            print(f"\n\nPBFT Consensus Successful -> Took {execution_time}s")
        else:
            print(f"\n\nPBFT Consensus Failed -> Took {execution_time}s")
        

