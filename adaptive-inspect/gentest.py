import modelTopology
import adaptiveInspect
import random
import time

scT1=modelTopology.scTopology()
                                #generate a new graph
#scT1.scInterface.genLinear(20)


scT1.scInterface.genGraphs(30)


#print(scT1.scInterface.kmap.edges())
scT1.scInterface.drawTree(scT1.scInterface.sc)
scT1.scInterface.drawTree(scT1.scInterface.kmap)
