import PBFT


x = PBFT.PBFTAggregator(8, 1)

print(x.getClusters())
print(x.getCommanderNodes())
print(x.getByzantineNodes())