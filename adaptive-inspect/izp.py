 #izp technique agnostic
# sc graph model for inspection
#t welsh

import networkx as nx
import matplotlib.pyplot as plt
import random


class asset:

	#An asset has:
	#	-type : (e.g. physical, digital, human, meta etc.)
	#			desc:   which determines the inspection techniques that can be employed on it
	#			future:
	#
	#    - intrusiveness constraint (integer)
	#			which reduces the efficacy of infoligence gathering
	#			OR prevents infoligence where technique intrusiveness > intrusive constraint
	#

	def __init__(self,name=random.randint(0,100),minCost=2,assetType=0,value=1):
		self.name=name
		self.assetType=assetType #0=physical, 1=cyber, 2=human
		self.minCost=minCost #intrusiveness
		self.value=value

	def function(self):
		#override with process function
		return 0



class SupplyChain:

	#A SupplyChain is a DiGraph containing assets of different types

	def __init__(self):
		self.sc=nx.DiGraph()
		self.nodes=self.sc.nodes
		#global intrusive constraint i.e. law enforcement?

	def randomSC(self,size=5):#
		#assets=[]
		for n in range(size):
			temp=asset(n)
			#assets.append(t)
			if n == 0:
				self.sc.add_node(n,d=temp)

			else:
				self.sc.add_node(n,d=temp)
				self.sc.add_edge(n-1,n,weight=0.5)

	def addAsset(self,name=None,i=None,assetType=0):
		if name is None:
			name=random.randint(0,1000)
		temp=asset(name,i,assetType)
		self.sc.add_node(name,d=temp)


	def allSolutions(self):
		#generate all subgraphs
		return 0

	def getAssetType(self,asset):
		return self.sc.node[asset]['d']

	def setAssetType(self,asset,assetType):
		self.sc.nodes[asset]['d'].assetType=assetType

	def setAssetMaxIntrusive(self,asset,intru):
		self.sc.nodes[asset]['d'].maxIntrusive=intru

	def setAssetInspectionCost(self,asset,cost):
		self.sc.nodes[asset]['d'].cost=cost

	def addLink(self,a1,a2,direction,weight):
		self.sc.add_edge(a1,a2,weight=weight)
		if direction=='bi':
			self.sc.add_edge(a2,a1,weight=weight)

	def delLink(self,a1,a2):
		self.sc.remove_edge(a1,a2)



class inspect:
	#functions for reasoning about inspection strategies:

	# - check the base "value" of a node or subgraph according to the graph structure
	# - check if a solution meets an intrustive techniques

	def __init__(self,sc=None):
		#self.techniques=[]
		self.scTarget=sc
		self.values={}
		self.costs={}
		self.flags={}
		self.suspectNodes=[2,1]
		self.data={}


	#def calcDirect(self,node):
		#pass

	def calcCosts(self,node):
		pass

	def genInit(self):
		self.calcValueCentrality()
		for n in sc1.nodes:
			insp1.flags[n]=1
		for n in self.scTarget.nodes():
			#node : 0 values,1 costs,2 flags
			self.data[n]=[self.values[n],0,1]

	def upData(self):
		for n,v in self.data.items():
			self.data[n][0]=self.values[n]
			self.data[n][1]=self.costs[n]
			self.data[n][2]=self.flags[n]

	def calcValueIOCentrality(self,sc):
		value={}
		invalue=nx.in_degree_centrality(self.scTarget.sc)
		outvalue=nx.out_degree_centrality(self.scTarget.sc)
		print(invalue)
		for k in invalue:
			value[k]=((invalue[k]+outvalue[k])/2)
		self.IOValues=value

	def calcValueCentrality(self):
		self.values=nx.degree_centrality(self.scTarget.sc)



	def checkinfo(self,values):
		#For a set of nodes, return
		validCases=[]
		for a in self.scTarget.sc.nodes:
			print("Asset: %s Value: %f" % (a,values[a]))
			i=0
			#for t in techniques:
			#	i+=1
			print("Techique:%d, info:%f, Cost:%d, Result:%d" % (i,t[0]*values[a],t[1],self.checkIntrusive(a,t)))
			print("")
		return validCases

	def nextInsp(self,solution):
	#	print("\nInspection")
		for s in solution:
			if s[0] in self.suspectNodes:

				#set in nodes to 2
				#inout=self.scTarget.sc.in_edges(s[0])+self.scTarget.sc.out_edges(s[0])
			#	print(self.scTarget.sc.in_edges(s[0]))
			#	print(self.scTarget.sc.out_edges(s[0]))
				for n in self.scTarget.sc.in_edges(s[0]):			#DOUBLE CHECK
					if self.flags[n[0]]==1:
						self.flags[n[0]]=2
				for n in self.scTarget.sc.out_edges(s[0]):
					if self.flags[n[0]]==1:
						self.flags[n[1]]=2

				self.flags[s[0]]=-1
			else:
				self.flags[s[0]]=0
#		print("Flags: ")
#		print(self.flags)

		return(self.flags)

	def printData(self,dict):
		self.upData()
		print("Node\tValue\tCost\tFlag")
		for k,v in dict.items():
			val,cost,flag = v
			print("{:d}\t{: .1f}\t{: .1f}\t{:d}".format(k,val,cost,flag))


	def greedySearch(self,sc,maxCost):
		#Given a supply chain graph
		#Search for an optimum solution: an inspection zone (subgraph) and inspection technique which:
			# max(infoligence) :  (infoligence is structural value + asset value) * technique infoligence
		#Within constraints of:
			# intrusiveness : solve for technique intrusivness <= asset + global (zone etc.)
			# cost
		poss=[]
		solution=[]
		priority=[]
		tempcost=0
		#first check flags
		for k,v in self.flags.items():
			if self.flags[k]==2:
				priority.append(k)
			elif self.flags[k]==1:
				poss.append(k)

		for p in priority:							#first try to add those flagged as high priority
			if tempcost+self.costs[p] <= maxCost:
				solution.append((p,self.values[p],self.costs[p]))
				tempcost=tempcost+self.costs[p]

		if tempcost < maxCost:
			sortval=dict(sorted(self.values.items(), key=lambda item: item[1],reverse=True))
		#print(sortval)

		for k, v in sortval.items():
			if(k in poss):
				if (self.costs[k] + tempcost) <= maxCost:
					solution.append((k,self.values[k],self.costs[k]))
					tempcost=tempcost+self.costs[k]
		#print(self.checkinfo(self.values,techniques))
		#print("Solution")
		#print(solution)
		return solution



#technique has a level of infoligence gathered and a level of intrusiveness (TODO: should also reflect a type/interface)
#techniques=[(1,1),(2,1),(3,2),(3,2)]
#techniques require multiple assets


sc1=SupplyChain()
sc1.randomSC(5)
insp1=inspect(sc1)
#add a cyber node
sc1.addAsset(5,2)
#sc1.setAssetType('C1',1) #set to cyber
#sc1.setAssetMaxIntrusive('C1',3)
sc1.addLink(2,5,'n',0.5)
sc1.addLink(5,4,'n',0.5)

insp1.genInit()



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
insp1.printData(insp1.data)

#insp1.calcCosts()
#print(values)
#value=nx.degree_centrality(sc1.sc)

input()
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
insp1.printData(insp1.data)

input()
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
insp1.printData(insp1.data)

input()
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
insp1.printData(insp1.data)

input()
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)
insp1.printData(insp1.data)

input()
#topology change
insp1.flags[1]=1
insp1.flags[2]=1
insp1.suspectNodes=[]
print("Topology Change")
greedy=insp1.greedySearch(sc1.sc,1)
insp1.nextInsp(greedy)



#insp1.checkinfo(insp1.calcValueIOCentrality(),techniques)
#nx.draw_kamada_kawai(sc1.sc,with_labels=True)
#nx.draw_spectral(sc1.sc,with_labels=True)
#nx.draw_spring(sc1.sc,with_labels=True)
#nx.draw_shell(sc1.sc,with_labels=True)
#print(list(nx.weakly_connected_components(sc1.sc)))
#
