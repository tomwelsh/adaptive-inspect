import networkx	as nx
import matplotlib.pyplot as plt
import random

class SupplyChainInterface:

	#A SupplyChain is a DiGraph containing assets of different types

	def __init__(self):
		self.sc=nx.DiGraph()
		self.nodes=self.sc.nodes
		self.containers=[]
		self.kmaps={}   #maps between kontainers k and processes and k
		self.pmaps={}
		#global intrusive constraint i.e. law enforcement?

	def setAssetModel(self,assModel):
		self.assetModel=assModel

	def randomSC(self,size=5):#
		#assets=[]
		for n in range(size):
			temp=self.assetModel.asset(n)
			#assets.append(t)
			if n == 0:
				self.sc.add_node(n,d=temp)

			else:
				self.sc.add_node(n,d=temp)
				self.sc.add_edge(n-1,n,weight=0.5)

	def drawGraph(self):
		nx.draw(self.sc)
		print(self.sc)
		plt.show()


	def genLinear(self,size):
		self.sc=nx.gn_graph(size) #best
		#print(self.sc.nodes())
		#self.sc=nx.gnc_graph(10) #bad
		#self.sc=nx.random_k_out_graph(10,1,0.5)
		#self.sc=nx.scale_free_graph(10)


	def genContainers(self,p=0.1,tl=4):


		#this is hacky, bidirectional dictionaries, memory usage?!


		#categorise containment relationships
		#package in lorry
		#machines in factroy
		#proceses in server

		contTypes={'rooms':0, 'servers':0}

		#for each cell:
		#if cell is not in a container
		# if prob random.random() > probContained:
		#if cell is adjacent to a cell in a container
			#add to container
		#else:
			#create new container
		#self.containers.append(0)



		print(self.sc.nodes)
		for i in range(len(self.sc.nodes)):
			n=random.choice(list(self.sc.nodes.keys()))
			if n not in self.pmaps:
				if random.random() > p:
					if (n+1) in self.pmaps:
						self.pmaps[n]=self.pmaps[n+1]
						self.kmaps[self.pmaps[n]].append(n)
					elif n-1 in self.pmaps:
						self.pmaps[n]=self.pmaps[n-1]
						self.kmaps[self.pmaps[n]].append(n)
					else:
						#create new container ##this should be in reverse
						if len(self.kmaps)==0:
							self.pmaps[n]=0
							self.kmaps[0]=[n]
						else:
							self.kmaps[len(self.kmaps)]=[n]
							self.pmaps[n]=len(self.kmaps)
			print(self.kmaps)
			print(self.pmaps)





	def addAsset(self,name=None,i=None,assetType=0):
		if name is None:
			name=random.randint(0,1000)
		temp=self.assetModel.asset(name,i,assetType)
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
