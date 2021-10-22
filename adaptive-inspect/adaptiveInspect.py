import networkx as nx
import random

class inspect:
	#functions for reasoning about inspection strategies:

	# - check the base "value" of a node or subgraph according to the graph structure
	# - check if a solution meets an intrustive techniques

	def __init__(self,sc=None):
		#self.techniques=[]
		self.scTarget=sc
		self.scHist={}
		self.values={}
		self.costs={}
		self.flags={}
		self.suspectNodes=[]
		self.found=[]
		self.contCostM=0


	def initTopHist(self):
		for node in self.scTarget.sc.nodes:
			self.scHist[node]=self.hashNode(node)
			self.flags[node]=1
			self.values[node]=1

	def monitorTopology(self):
		changedNodes=[]
		#For each node in topology,
		#if the hash matches previous:
		#	update the history and return a list of all changed nodes

		for node in self.scTarget.sc.nodes:
			if self.hashNode(node) != self.scHist[node]:
				changedNodes.append(node)
				#print("changed")
				self.scHist[node]=self.hashNode(node)
				self.flags[node]=1
		return changedNodes

	def hashNode(self,node):
		return hash(str(node))

	def analyseValue(self,c):
		# Set centrality values
		# Add contextual multipliers
		#
		if c==3:
			self.calcValueCentrality()
		elif c==1:
			self.calcInCentrality()
		elif c==2:
			self.calcOutCentrality()
	#	self.calcContextualValue()


	def planInspection(self):
		return self.greedySearch(self.scTarget,1)


	def executeInspection(self,solution,adjFlag=0,perFlag=False):
		#print("\nInspection")
	#	print(solution)
		for s in solution:
			if adjFlag>0:
				for n in self.scTarget.sc.in_edges(s[0]):
					if n[0] in self.suspectNodes:
						if self.flags[n[0]]==1:
							self.flags[n[0]]=2
				#for n in self.scTarget.sc.out_edges(s[0]):   #should remove?l$
				#	if n[1] in self.suspectNodes:
				#		if self.flags[n[0]]==1:
				#			self.flags[n[1]]=2

			if s[0] in self.suspectNodes:
				self.flags[s[0]]=-1
				self.found.append(s[0])
				#set in nodes to 2
				#inout=self.scTarget.sc.in_edges(s[0])+self.scTarget.sc.out_edges(s[0])
			#	print(self.scTarget.sc.in_edges(s[0]))
			#	print(self.scTarget.sc.out_edges(s[0]))

			#CHECK IF CONNECTED TO SUSPECT NODES


			else:
				self.flags[s[0]]=0


	def tweakNodes(self,ratio):
		#
		#print(round((len(self.scHist)-1)*ratio))
		for i in range(round((len(self.scHist)-1)*ratio)):
			#print("changed")
			n=random.randint(0,len(self.scHist)-1)
			if n not in self.suspectNodes:
				self.scHist[n]=0



	def randomCosts(self,rtype='gauss'):
		#print(len(self.costs)-1)
		for i in self.scTarget.sc.nodes:
			if rtype=='gauss':
				self.costs[i]=random.gauss(0,1)
			else:
				self.costs[i]=random.random()

	def tweakCosts(self):
		self.costs[random.randint(len(self.costs))-1]=random.random()

	def calcCosts(self,node,cost):
		#set a simulated value
		self.costs[node]=cost

	def calcValueIOCentrality(self,sc):
		value={}
		invalue=nx.in_degree_centrality(self.scTarget.sc)
		outvalue=nx.out_degree_centrality(self.scTarget.sc)

		#print(invalue)
		for k in invalue:
			value[k]=((invalue[k]+outvalue[k])/2)
		self.IOValues=value

	def calcOutCentrality(self):
		self.values=nx.out_degree_centrality(self.scTarget.sc)

	def calcInCentrality(self):
		self.values=nx.in_degree_centrality(self.scTarget.sc)

	#	print(self.values)

	def calcValueCentrality(self):
		self.values=nx.degree_centrality(self.scTarget.sc)

	def calcConnectedValue(self,n):
		#we compound the value of in node connections
		value=0
		for n in self.scTarget.sc.in_edges(n):
			value=value+(self.values[n]/2)
		return value

	def calcContainedCost(self,node):
		tempCosts={}
		nodes=self.scTarget.getContained(self.scTarget.getContainer(node))
		for n in nodes:
				tempCosts[n[1]]=self.costs[n[1]]*self.contCostM
		return tempCosts

	def setContextualValue(self,node,cval):
		#for i in range(len(self.sc))
		pass

	def inspectionInstance(self,node):
		# TODO: create an instance to reason about possibilities
		pass

	def greedySearch(self,sc,maxCost):
		#Given a supply chain graph
		#Search for an optimum solution: an inspection zone (subgraph) and inspection technique which:
			# max(infoligence) :  (infoligence is structural value + asset value) * technique infoligence
		#Within constraints of:
			# intrusiveness : solve for technique intrusivness <= asset + global (zone etc.)
			# cost
		#greedy->local?
		#maxIntr=5
		#globinfo=0
	    #values=self.calcValueIOCentrality(sc)   #structural value of nodes
		#get all valid cases
		poss=[]
		solution=[]
		priority=[]
		tempcost=0
		newCosts={}


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
				if self.contCostM!=0:
					containedCosts=self.calcContainedCost(p)
				#	print(containedCosts)
					for c in containedCosts:			#update new contained costs
						#print(self.costs[c])
						#print(containedCosts[c])

						newCosts[c]=containedCosts[c]

		#we update all costs according to priority NODES

		if tempcost < maxCost:
			sortval=dict(sorted(self.values.items(), key=lambda item: item[1],reverse=True))
		#print(sortval)

		#print(sortval)
	#	print(self.costs)
		for k, v in sortval.items():
			if(k in poss):
			#	print(k)
			#	print(v)
			#	print(self.costs[k])
				kcost=self.costs[k]
			#	print(kcost)
				if k in newCosts:
				#	print('old'+str(kcost))
				#	print('n'+str(newCosts[k]))
					kcost=newCosts[k]
					#print(k)
				if (kcost + tempcost) <= maxCost:
					solution.append((k,self.values[k],kcost))
					tempcost=tempcost+kcost
					if self.contCostM!=0:
						containedCosts=self.calcContainedCost(k)
						for c in containedCosts:			#update new contained costs
							newCosts[c]=containedCosts[c]
		#print(self.checkinfo(self.values,techniques))
		#print("Solution")
	#	print(solution)
		return solution
