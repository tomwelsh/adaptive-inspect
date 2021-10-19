import modelTopology
import adaptiveInspect
import random
import time

scT1=modelTopology.scTopology()
                                #generate a new graph
scT1.scInterface.genLinear(20)
scT1.scInterface.genContainers()
print(scT1.scInterface.containers)
print(scT1.scInterface.kmaps)
print(scT1.scInterface.pmaps)
scT1.scInterface.drawGraph()
