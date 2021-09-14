import modelTopology
import adaptiveInspect
import random


#create combined topology



#AInsp loop
result=0
for j in range(100):
    scT1=modelTopology.scTopology()

    #generate a new graph
    size=10
    scT1.scInterface.genLinear(size)
    #sc1.scInterface.drawGraph()


    #create a new adaptive inspection instance
    insp1=adaptiveInspect.inspect(scT1.scInterface)

    insp1.suspectNodes.append(random.randint(0,size-1))
    for i in range(size):
        insp1.costs[i]=0.5
    insp1.initTopHist()
    found=False
    i=0
    while found is not True:
        i=i+1
        insp1.monitorTopology()
        insp1.analyseValue()
        plan=insp1.planInspection()
        insp1.executeInspection(plan,True)
        if insp1.found==insp1.suspectNodes:
            found=True
    #print(i)
    result=result+i
print(result/10)
