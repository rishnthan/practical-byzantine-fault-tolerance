import random
import aiohttp


replies_list = []

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
    def receiveReplies(json):
        replies_list.append(json)

    @staticmethod
    def checkReplies():
        num_of_msg_corrupted = replies_list.count("Corrupt")
        num_of_msg_correct = replies_list.count("very-important-data")
        if num_of_msg_correct > num_of_msg_corrupted:
            return "Consensus Reached: Result > Correct Data"
        else:
            return "Consensus Reached: Result > Corrupt Data"