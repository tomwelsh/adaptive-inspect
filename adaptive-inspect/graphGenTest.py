import modelTopology
import adaptiveInspect
import random
import time

#create combined topology



#AInsp loop
#experiment parameters
netSizes=[20]
randomCosts=[True]
valueAnalysis=[True,False]
nodeTweak=[0,0.1,0.2]#,0.3,0.4]
#adj=[True,False]
monitor=[True,False]
container=[0,0.6,0.8]
centr=[0,1] #0 is none, 1 is in, 2 is out, 3 is both
basecosts=0.5
#costTweak=[0,1,2,3,4,5]
runs=10
timeout=10
avgs=open(("avgs%f" % time.time()),'w')
dataSet=open("data%f"% time.time(),'w')
dataSet.write("NetSize,RandomCosts,ValueAnalysis,MonitorFlag,NodeTweak,AdjacencyFlag,contCost,Results")
avgs.write("NetSize,RandomCosts,ValueAnalysis,MonitorFlag,NodeTweak,AdjacencyFlag,contCost,Avg")

for size in netSizes:
    for rCosts in randomCosts:
        for v in valueAnalysis:
            for m in monitor:
                for contCost in container:   #increase or not in contCost
                    for nTweak in nodeTweak:
                        for cent in centr:  #centrality flag
                            dataSet.write("\n%d,%s,%s,%s,%f,%d,%f" % (size,rCosts,v,m,nTweak,cent,contCost))
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
                                for i in range(size):
                                    insp1.costs[i]=basecosts
                                if rCosts==True:
                                    insp1.randomCosts('asd  ')

                                insp1.initTopHist()

                                found=False
                                i=0
                                while found is not True:
                                    i=i+1
                                    if m==True:
                                        insp1.monitorTopology()
                                    if v==True:
                                        insp1.analyseValue(cent)

                                    insp1.contCostM=contCost
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
                            avgs.write("\n%d,%s,%s,%s,%f,%d,%f,%d" % (size,rCosts,v,m,nTweak,cent,contCost,result/runs))
                            avgs.flush()
                            print(result/runs)#
dataSet.close()
avgs.close()
