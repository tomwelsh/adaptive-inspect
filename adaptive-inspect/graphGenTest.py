import modelTopology
import adaptiveInspect
import random
import time

#create combined topology



#AInsp loop
#experiment parameters
netSizes=[100]
randomCosts=[0.3,0.5,1]
nodeTweak=[0]#,0.3,0.4]
#adj=[True,False]
monitor=[False]
container=[0.1,0.5]
centr=[0,1] #0 is none, 1 is in, 2 is out, 3 is both
#costTweak=[0,1,2,3,4,5]
runs=100
timeout=10
avgs=open(("avgs%f" % time.time()),'w')
dataSet=open("data%f"% time.time(),'w')
dataSet.write("NetSize,RandomCosts,MonitorFlag,NodeTweak,AdjacencyFlag,CalcCentr,contCost,Results")
avgs.write("NetSize,RandomCosts,MonitorFlag,NodeTweak,AdjacencyFlag,CalcCentr,contCost,Avg")
calcCent=[True,False]

for calcC in calcCent:
    for size in netSizes:
        for rCosts in randomCosts:
            for m in monitor:
                for contCost in container:   #increase or not in contCost
                    for nTweak in nodeTweak:
                        for cent in centr:  #centrality flag
                            dataSet.write("\n%d,%s,%s,%f,%d,%s,%f" % (size,rCosts,m,nTweak,cent,calcC,contCost))
                            dataSet.flush()
                            results=[]
                            result=0
                            for j in range(runs):
                                scT1=modelTopology.scTopology()
                                #generate a new graph
                                scT1.scInterface.genConnect(size)
                                scT1.scInterface.genContainer()
                            #    scT1.scInterface.drawGraph()
                                #scT1.scInterface.drawGraph()
                                #create a new adaptive inspection instance
                                insp1=adaptiveInspect.inspect(scT1.scInterface)

                                insp1.suspectNodes.append(random.choice(list(scT1.scInterface.sc.nodes())))
                                if rCosts==1:
                                    insp1.randomCosts('asd  ')
                                else:
                                    for n in scT1.scInterface.sc.nodes:
                                        insp1.costs[n]=rCosts
                                insp1.contCostM=contCost

                                insp1.initTopHist()

                                found=False
                                i=0
                                while found is not True:
                                    i=i+1
                                    if m==True:
                                        insp1.monitorTopology()
                                    if calcC==True:
                                        insp1.analyseValue(cent)


                                    plan=insp1.planInspection()
                                    insp1.executeInspection(plan,cent)

                                    if insp1.found==insp1.suspectNodes:
                                        found=True
                                    insp1.tweakNodes(nTweak)


                                    if i >= (size*timeout):
                                        i=size*timeout
                                        break
                                    #print(i)

                                dataSet.write
                                result=result+i
                                dataSet.write(",%d"%i)
                                #dataSet.write(",%d"%result/runs)
                            avgs.write("\n%d,%s,%s,%f,%d,%s,%f,%d" % (size,rCosts,m,nTweak,cent,calcC,contCost,result/runs))
                            avgs.flush()
                        #    print(result/runs)#
dataSet.close()
avgs.close()
