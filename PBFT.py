import random

# dictionary to collect replies of nodes after final stage of PBFT
replies_list = {}

# PBFT Aggregator Class
class PBFTAggregator:
    # Initiate the class
    def __init__(self, num_of_corrupt, type_of_byzantine, num_of_commanders=1):
        # saves class instance variables by calling the related functions
        self.nodes_list = self.nodes_list(num_of_corrupt)
        self.byzantine_nodes = self.byzantine_nodes(self.nodes_list, num_of_corrupt)
        self.commander_node = self.commander_node_selector(self.nodes_list, num_of_commanders)
        self.type_of_byzantine = self.type_of_byzantine(type_of_byzantine, self.byzantine_nodes, self.commander_node)
    
    # Generate node list
    def nodes_list(self, num_of_corrupt):
        nodes_list = []
        for i in range(0, 3*num_of_corrupt + 1):
            nodes_list.append(i)
        return nodes_list
    
    # Select Commander Node at random
    def commander_node_selector(self, nodes_list, num_of_nodes):
        commander_nodes_list = []
        temp_list = list(nodes_list)
        for i in range(num_of_nodes):
            commander_node = random.choice(temp_list)
            commander_nodes_list.append(commander_node)
            temp_list.remove(commander_node)
        return commander_nodes_list
    
    # Select Byzantine Nodes at random
    def byzantine_nodes(self, nodes_list, num_of_nodes):
        byzantine_nodes_list = []
        temp_list = list(nodes_list)
        for i in range(num_of_nodes):
            byzantine_node = random.choice(temp_list)
            byzantine_nodes_list.append(byzantine_node)
            temp_list.remove(byzantine_node)
        return byzantine_nodes_list
    
    # For offline byzantine node, make sure commander node is not byzantine
    def type_of_byzantine(self, type_of_byzantine, byzantine_nodes_list, commander_nodes_list):
        for i in commander_nodes_list:
            if i in byzantine_nodes_list and type_of_byzantine == 0:
                self.byzantine_nodes.remove(i)
                self.byzantine_nodes.append(random.choice(self.nodes_list))

    # Get nodes_list from class instance
    def getNodes(self):
        return self.nodes_list
    
    # Get byzantine_nodes from class instance
    def getByzantineNodes(self):
        return self.byzantine_nodes

    # Get commander_node from class instance
    def getCommanderNode(self):
        return self.commander_node
    
    # Initializes replies_list dictionary
    @staticmethod
    def initReplies(total_nodes):
        for i in range(total_nodes):
            replies_list[i] = []

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
    def checkReplies():
        for key, value in replies_list.items():
            num_of_corrupt = value.count("Corrupt")
            num_of_correct = len(replies_list[key]) - num_of_corrupt
            print(f"Node {key} -> {num_of_correct} Correct {num_of_corrupt} Corrupt")
