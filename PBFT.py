import random
import aiohttp

replies_list = {}

class PBFTAggregator:
    def __init__(self, num_of_corrupt, num_of_commanders=1):
        self.nodes_list = self.nodes_list(num_of_corrupt)
        self.byzantine_nodes = self.byzantine_nodes(self.nodes_list, num_of_corrupt)
        self.commander_node = self.commander_node_selector(self.nodes_list, num_of_commanders)
        self.nodes = []
        
    def nodes_list(self, num_of_corrupt):
        nodes_list = []
        for i in range(0, 3*num_of_corrupt + 1):
            nodes_list.append(i)
        return nodes_list

    def byzantine_nodes(self, nodes_list, num_of_nodes):
        byzantine_nodes_list = []
        temp_list = list(nodes_list)
        for i in range(num_of_nodes):
            byzantine_node = random.choice(temp_list)
            byzantine_nodes_list.append(byzantine_node)
            temp_list.remove(byzantine_node)
        return byzantine_nodes_list
    
    def commander_node_selector(self, nodes_list, num_of_nodes):
        commander_nodes_list = []
        temp_list = list(nodes_list)
        for i in range(num_of_nodes):
            commander_node = random.choice(temp_list)
            commander_nodes_list.append(commander_node)
            temp_list.remove(commander_node)
        return commander_nodes_list
    
    def getNodes(self):
        return self.nodes_list
    
    def getByzantineNodes(self):
        return self.byzantine_nodes

    def getCommanderNode(self):
        return self.commander_node

    async def request(self, message):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http:localhost:{8080 + self.commander_node}/receive', json=message) as response:
                print(f"Response: {response.status}")
    
    @staticmethod
    def initReplies(total_nodes):
        for i in range(total_nodes):
            replies_list[i] = []

    @staticmethod
    def receiveReplies(data):
        replies_list[data[0]].append(data[1])
    
    @staticmethod
    def checkReplies():
        for key, value in replies_list.items():
            num_of_corrupt = value.count("Corrupt")
            num_of_correct = value.count("very-important-data")
            print(f"Node {key} -> {num_of_correct} Correct {num_of_corrupt} Corrupt")
