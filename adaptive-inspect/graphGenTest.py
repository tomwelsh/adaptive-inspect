import modelTopology
import adaptiveInspect
import random


#create combined topology
scT1=modelTopology.scTopology()

#generate a new graph
size=20
scT1.scInterface.genLinear(size)
#sc1.scInterface.drawGraph()


#create a new adaptive inspection instance
insp1=adaptiveInspect.inspect(scT1.scInterface)
print(scT1.scInterface.sc.nodes())

insp1.suspectNodes.append(random.randint(0,size))
print(insp1.suspectNodes)

for i in range(size):
    insp1.costs[i]=0.5
insp1.initTopHist()
#AInsp loop
for i in range(10):
    insp1.monitorTopology()
    insp1.analyseValue()
    plan=insp1.planInspection()
    insp1.executeInspection(plan)
