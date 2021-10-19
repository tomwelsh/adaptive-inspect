import modelTopology
import adaptiveInspect
import random
import time

scT1=modelTopology.scTopology()
                                #generate a new graph
scT1.scInterface.genLinear(10)
scT1.scInterface.genContainers()
print(scT1.scInterface.kmap.edges())
scT1.scInterface.drawGraph(scT1.scInterface.kmap)
