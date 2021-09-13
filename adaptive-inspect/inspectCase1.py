import adaptiveInspect
import modelTopology

#example adaptive inspection cases
sc1=modelTopology.scTopology()
sc1.sc.randomSC(5)
insp1=adaptiveInspect.inspect(sc1.sc)
#add a cyber node
sc1.sc.addAsset(5,2)
#sc1.setAssetType('C1',1) #set to cyber
#sc1.setAssetMaxIntrusive('C1',3)
sc1.sc.addLink(2,5,'n',0.5)
sc1.sc.addLink(5,4,'n',0.5)
insp1.calcValueCentrality()

for n in sc1.sc.nodes:
	insp1.flags[n]=1

#sc1.setAssetMaxIntrusive('C1',1)
#sc1.setAssetMaxIntrusive(3,1)
#add contextual values
insp1.values[4]=insp1.values[4]*0.5
insp1.values[1]=insp1.values[1]*1.2
insp1.costs[0]=0.4
insp1.costs[1]=0.46
insp1.costs[2]=0.57
insp1.costs[3]=0.89
insp1.costs[4]=0.59
insp1.costs[5]=0.89



#print(insp1.flags)

#insp1.calcCosts()
#print(values)
#value=nx.degree_centrality(sc1.sc)
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)

#topology change
insp1.flags[1]=1
insp1.flags[2]=1
insp1.suspectNodes=[]
print("Topology Change")
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
