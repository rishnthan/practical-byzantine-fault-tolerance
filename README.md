# Practical Byzantine Fault Tolerance

## Table of Contents
1. Information
2. Requirements
3. How-to Test
4. Notes

## 1.0 Information
This is a simple implementation in Python of the well-known Practical Byzantine Fault Tolerance (PBFT) consensus algorithm [[1]](https://pmg.csail.mit.edu/papers/osdi99.pdf). PBFT was designed as a method to solve the Byzantine General's Problem [[2]](https://www.microsoft.com/en-us/research/publication/byzantine-generals-problem/) in a distributed system. 

There are a few types of byzantine faults:-
1. Failure to return a result
2. Respond with the wrong or misleading result
3. Respond with varying results to different nodes in the system

The faults are simplified into two, offline (failure to return a result) and malicious/falsifying (responding with a wrong result or giving varying results to different nodes). For the sake of simplicity, the normal malicious nodes and commander malicious nodes have separate behaviour. The normal malicious node will respond with the wrong result, while the commander malicious node will respond with varying results to different system nodes. 

## 2.0 Requirements
- Python >= 3.11.1
- Aiohttp >= 3.8.5
- curl >= 7.81.0

## 3.0 How-to Test

Run **`python main.py`** to establish the nodes within the network.

***Example***
```
C:\practical-byzantine-fault-tolerance> python main.py
Total Nodes: 4 -> [0, 1, 2, 3]
Byzantine Nodes: 1  -> [2]
Commander Node: 1 -> [0]

 Starting Nodes

Node 0 started on http://0.0.0.0:8080
Node 1 started on http://0.0.0.0:8081
Node 2 started on http://0.0.0.0:8082
Node 3 started on http://0.0.0.0:8083

Node 0 is the commander node.        
Running on http://0.0.0.0:8080  
``` 
This output shows the number of nodes within the system, which nodes are byzantine and which are commander, the URL for each node, and the commander node's URL.

You can test each node's status by using the endpoint `/status` with curl to see if it is online or offline such as follows: **`curl http://localhost:8080`**

Finally, to initiate the PBFT consensus send a **POST** request with a JSON file containing
```
{"data": "anything-here-doesnt-matter"}
```
to the commander node's URL with the endpoint `/preprepare`. The following command can be used to test the commander node: **`curl -X POST -H "Content-Type: application/json" -d '{"data": "very-important-data"}' http://localhost:{commander port}/preprepare`**. Please change the commander port as necessary.

Once consensus is reached, the execution time of the algorithm will be outputted along with the results replies from the nodes.

***Example***
```
PBFT Consensus Time: 0.050912s
Node 0 -> 4 Correct 3 Corrupt
Node 1 -> 5 Correct 2 Corrupt
Node 2 -> 5 Correct 2 Corrupt
Node 3 -> 4 Correct 2 Corrupt
```

## 4.0 Notes
Things to note.
1. This is a **simple** implementation of the consensus model.
2. To change the number of byzantine nodes or the type of byzantine nodes existing within the system must be changed manually.
