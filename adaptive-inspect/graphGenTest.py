import modelTopology
import adaptiveInspect
import random


#create combined topology



#AInsp loop
result=0
runs=100
for j in range(runs):
    scT1=modelTopology.scTopology()

    #generate a new graph
    size=100
    scT1.scInterface.genLinear(size)
    #scT1.scInterface.drawGraph()


    #create a new adaptive inspection instance
    insp1=adaptiveInspect.inspect(scT1.scInterface)

    insp1.suspectNodes.append(random.randint(0,size-1))
    for i in range(size):
        insp1.costs[i]=0.1

    insp1.randomCosts()
    insp1.initTopHist()
    found=False
    i=0
    while found is not True:
        i=i+1
        #if ((i % 1) == 0):
        #    insp1.randomCosts()
            #print(insp1.costs)
        insp1.monitorTopology()
        insp1.analyseValue()
        plan=insp1.planInspection()
        insp1.executeInspection(plan,True)
        if insp1.found==insp1.suspectNodes:
            found=True
        #print(insp1.found)
        #print(insp1.suspectNodes)
        #print(insp1.values)
        insp1.tweakNodes(0.1)
        #if i > size: break
    print(i)
    result=result+i

print(result/runs)
