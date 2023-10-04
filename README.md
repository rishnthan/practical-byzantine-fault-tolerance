# Practical Byzantine Fault Tolerance

## Table of Contents
1. [Information](#1-Information)
2. Requirements
3. How-to test
4. Notes

## 1. Information
This is a simple implementation of the well-known Practical Byzantine Fault Tolerance (PBFT) consensus algorithm [[1]](https://pmg.csail.mit.edu/papers/osdi99.pdf). PBFT was designed as a method to solve the Byzantine General's Problem [[2]](https://www.microsoft.com/en-us/research/publication/byzantine-generals-problem/) in a distributed system.

There are a few types of byzantine faults
1. Failure to return a result
2. Respond with wrong or misleading result
3. Respond with varying result to different nodes in the system

For the purpose of this implementation, 