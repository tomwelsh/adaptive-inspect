import networkx	as nx
import matplotlib.pyplot as plt
import random

class SupplyChainInterface:

	#A SupplyChain is a DiGraph containing assets of different types

	def __init__(self):
		self.sc=nx.DiGraph()    #supply chain, connection graph

		self.kmap=nx.DiGraph()   #containment map, place graph
		self.nodes=self.sc.nodes
		#self.kmaps={}   #maps between kontainers k and processes and k
		#self.pmaps={}

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

	def drawGraph(self,g):
		nx.draw(g,with_labels=True)
		print(g)
		plt.show()


	def drawTree(self,g):
		from networkx.drawing.nx_pydot import graphviz_layout

		pos = graphviz_layout(g, prog="dot") #dot #circo
		nx.draw(g,pos,with_labels=True)
		plt.show()


	def bfs(self,G):
		#http://www.ics.uci.edu/~eppstein/PADS/BFS.py
		#breadth first search
		remapped={0:'1'}
		visited = set()
		root=0
		currentLevel = [root]
		while currentLevel:
			for v in currentLevel:
				visited.add(v)
			nextLevel = set()
			levelGraph = {v:set() for v in currentLevel}
			for v in currentLevel:
				for w in G[v]:
					if w not in visited:
						levelGraph[v].add(w)
						nextLevel.add(w)
			yield levelGraph
			currentLevel = nextLevel


	def genLinear(self,size):
		self.sc=nx.gn_graph(size) #best
		remapped={}
		r=self.bfs(self.sc.to_undirected())
		level=0
		inc=0
		lists={}
		for l in list(r):
			#print(l)
			inc=0
			print(level)
			#print(list(l))
			for n in list(l):
				remapped[n]="%d.%d" % (level,inc)
				inc=inc+1

			level=level+1

		self.sc=nx.relabel_nodes(self.sc, remapped)
		#self.sc=nx.gnc_graph(10) #bad
		#self.sc=nx.random_k_out_graph(10,1,0.5)
		#self.sc=nx.scale_free_graph(10)




	def genGraphs(self,size):
		self.genLinear(size)
		#this is hacky, bidirectional dictionaries, memory usage?!
		#categorise containment relationships
		#package in lorry
		#machines in factroy
		#proceses in server
		factory=0.3
		rooms=2
		jitter=0.001
		#for each cell:
		#if cell is not in a container
		# if prob random.random() > probContained:
		#if cell is adjacent to a cell in a container
			#add to container
		#else:
			#create new container
		#self.containers.append(0)
		self.kmap.add_node('SC')
		#print(int(size*(factory+random.uniform(0,jitter))))
		for f in range(int(size*(factory+random.uniform(0,jitter)))):   #add fact
				self.kmap.add_edge('SC',('f%d' % f))
				for r in range(int((rooms+random.uniform(0,jitter)))):	#add rooms
					self.kmap.add_edge(('f%d' % f),('f%dr%d' % (f,r)))
		f=0
		rIndex=0
		pIndex=0
		#print(list(self.kmap.out_edges('f%d' % f))[rIndex][1])
		#print(list(self.kmap.out_edges('f%d' % f)))
	#	nodes=list(reversed(self.sc.nodes))
		for n in list(self.sc.nodes):
			if n !='SC':
				magicball=random.random()
				if magicball <= 0.3:    #increment R
	#				self.kmap.add_edge(('f%d' % f),n)
					#if can, increment R
					if rIndex+1 < len(list(self.kmap.out_edges('f%d' % f))):
						rIndex=rIndex+1
				elif 0.3 <= magicball <= 0.5:			#Increment F
					if f+1 < len(list(self.kmap.out_edges('SC'))):
						f=f+1
						rIndex=0
				else:
					pass
			#	print(list(self.kmap.out_edges('f%d' % f))[rIndex][1])
				self.kmap.add_edge(list(self.kmap.out_edges('f%d' % f))[rIndex][1],n)
				#self.sc.add_edge(pIndex,pIndex+1)
				pIndex=pIndex+1

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
