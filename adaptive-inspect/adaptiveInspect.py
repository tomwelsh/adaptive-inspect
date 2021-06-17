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


	#def calcDirect(self,node):
		#pass

	def monitorTopology():
		for nodes in self.targetTopology:

		pass

	def analyseValue():
		pass

	def planInspection():
		pass

	def executeInspection():
		pass

	def calcCosts(self,node):
		pass

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
		print("\nInspection")
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
		print("Flags: ")
		print(self.flags)



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
		print("\n~~Greedy Search~~\n")
		print("Values:")
		print(self.values)
		print("Costs:")
		print(self.costs)
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
		print("Solution")
		print(solution)
		return solution
