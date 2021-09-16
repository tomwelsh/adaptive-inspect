import modelTopology
import adaptiveInspect
import random
import time

#create combined topology



#AInsp loop
#experiment parameters
netSizes=[50]
randomCosts=[False,True]
valueAnalysis=[True,False]
nodeTweak=[0,0.1,0.2,0.3]#,0.3,0.4]
adj=[True,False]
basecosts=0.5
#costTweak=[0,1,2,3,4,5]
runs=100
avgs=open(("avgs%f" % time.time()),'w')
dataSet=open("data%f"% time.time(),'w')
dataSet.write("NetSize,RandomCosts,ValueAnalysis,NodeTweak,AdjacencyFlag,Results")
for size in netSizes:
    for rCosts in randomCosts:
        for v in valueAnalysis:
            for nTweak in nodeTweak:
                    for aFlag in adj:
                        dataSet.write("\n%d,%s,%s,%f,%s" % (size,rCosts,v,nTweak,aFlag))
                        dataSet.flush()
                        results=[]
                        result=0
                        for j in range(runs):
                            scT1=modelTopology.scTopology()
                            #generate a new graph
                            scT1.scInterface.genLinear(size)
                            #scT1.scInterface.drawGraph()
                            #create a new adaptive inspection instance
                            insp1=adaptiveInspect.inspect(scT1.scInterface)
                            insp1.suspectNodes.append(random.randint(0,size-1))
                            for i in range(size):
                                insp1.costs[i]=basecosts

                            if rCosts==True:
                                insp1.randomCosts('asd  ')


                            insp1.initTopHist()

                            found=False
                            i=0
                            while found is not True:
                                i=i+1
                                #if ((i % 1) == 0):   #this should be in tweakNodes?
                                #    insp1.randomCosts()
                                    #print(insp1.costs)
                                insp1.monitorTopology()
                                if v==True:
                                    insp1.analyseValue()
                                plan=insp1.planInspection()


                                insp1.executeInspection(plan,aFlag)
                                if insp1.found==insp1.suspectNodes:
                                    found=True
                                insp1.tweakNodes(nTweak)
                                if i >= (size*10):
                                    i=0
                                    break
                            #print(i)
                            dataSet.write
                            result=result+i
                            dataSet.write(",%d"%i)
                        #dataSet.write(",%d"%result/runs)
                        avgs.write("%d,%s,%s,%f,%s,%d\n" % (size,rCosts,v,nTweak,aFlag,result/runs))
                        avgs.flush()
                        print(result/runs)#
dataSet.close()
avgs.close()
