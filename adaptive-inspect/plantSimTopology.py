#Plantsim topology modeling functions

# + additional random python functionality

#SPARE@UL www.spare.lero.ie


#goals:

# parse - tick

# viz   - tick(ish)

# tweak?

# simulation?

# inspection

import win32com.client as win32
import networkx as nx #slow :(
import matplotlib.pyplot as plt
import adaptiveInspect
import modelSC
import time

class pSimTop:

	def __init__(self,filepath,rootModel,visible=False):
		dispatch_string = 'Tecnomatix.PlantSimulation.RemoteControl'
		self.plantsimCom = win32.Dispatch(dispatch_string)
		self.plantsimCom.SetVisible(visible)   #disable or enable plantsim gui
		self.plantsimCom.LoadModel(filepath)    
		self.rootModel=rootModel  #root in the model that we start at
		self.connectGraph=nx.Graph()  #topology connect graph
		self.containGraph=nx.Graph()  #toplogy containment graph
		self.matFlowNodes=[]
		self.infFlowNodes=[]

	def getVal(self,obj,val):
		#wrapper to get vals from objects
		return self.plantsimCom.GetValue("%s.%s" % (obj,val))

	def toggleDisplay(self,display,b):
		#turn an asset display on and off
		if b == True:
			self.plantsimCom.SetValue("%s.Active" % display, True)
		else:
			self.plantsimCom.SetValue("%s.Active" % display, False)

	def initDisplay(self,template,target):
		#initialise an asset's display with that of another
		ex.plantsimCom.ExecuteSimTalk("%s.DisplayPanel.setElements(%s)" % (target,template))	

	def setDisplay(self,obj,row,data):
		#set the element of an asset display in the simulation to a value
		self.plantsimCom.ExecuteSimTalk("param s: string ; .%s.DisplayPanel.setValue(%d,s)" % (obj,row),"\"%s\"" % data ) # fucking finally
		#self.plantsimCom.ExecuteSimTalk("%s.setValue(%s,\"%s\")" % (obj,row,data)) # works

	def dumpDisplay(self,obj,table):
		#return the elements of an assets display in the gui to a table in the simulation
		self.plantsimCom.GetValue("%s.DisplayPanel.getElements(%s)" % (obj,table))

	def setVal(self,obj,val,data):
		#wrappy mcwrapwrap
		self.plantsimCom.SetValue(("%s.%s" % (obj,val),data))

	def getTabRow(self,table,row,col):
		return self.plantsimCom.GetValue("%s[%s,%s]" % (table,row,col)) # array indexes start from 1!! wtf

	def start(self):
		#self ex
		self.plantsimCom.StartSimulation(".Models.Assembly1.EventController")

	def stop(self):
		#self ex
		self.plantsimCom.StopSimulation()

	def checkNodeType(self,node):
		# do some checks for object types which cant be called at run time or are related to the experiment e.g. tools, once clear: return type
		tmp=self.plantsimCom.GetValue(node) 

		if tmp != "*"+node:  #dirty hack to check if an info flow 
			return 'inf'  #information
		elif str(self.getVal(node,"Class")).find(".Tools.") > 0:			#check for tools, TODO: maybe we need to search for other types which block too
			return 'tool' 
		else:	
			return self.getVal(node,"InternalClassType")    #return the class type name

	def getContained(self,model):
		#return all assets contained within another
		nodes=[]
		numNodes=int(self.getVal(model,"NumNodes"))
		for i in range(numNodes):
			j=i+1
			nodes.append(self.getVal(model,"Node(%d)" % j).lstrip("*"))
		return nodes

	def genTop(self,node,contain,connect):
		#generate topology
		# recursive exit cond is end of containment array....

		for n in self.getContained(node):
			contain.add_edge(node,n)
			if self.checkNodeType(n) == 'Connector':
				connect.add_edge(*self.addConnect(n))
			elif self.checkNodeType(n) == 'Frame':    #only check for frames, maybe there are others or custom user types too
				self.genTop(n,contain,connect)

	def addConnect(self,node):
		#get the in and out edges of a node
		inNode=self.getVal(node,"pred").lstrip("*")
		outNode=self.getVal(node,"succ").lstrip("*")
		return (inNode,outNode)

	def drawGraph(self,graph):
		#basic networkx drawing
		nx.draw(graph, with_labels=True)
		plt.show()

	def writeGraph(self,graph,fname):
		#write to a file for use with external tools like gephi
		nx.write_gexf(graph,fname)

	def psDisconnect(self):
		#shutdown plantsim
		self.plantsimCom.Quit()

	def flagInpsect(self,n):
		pass





filepath="c:\\Users\\Tom\\Documents\\test2.spp" #location of plantsim model file
ex=pSimTop(filepath,".Models",True)    #load the plant sim topology instance

scInt=modelSC.SupplyChainInterface()    #model for adaptive inspection purposes

ex.genTop("Models.Assembly1",scInt.kmap,scInt.sc)   #generate the topology from the plantsim model and store in the supply chain interface

	### configure alerting by setting up display panel of assets
baseDisplay=".Models.Assembly1.MS1"     #clone the display elements to other stations
template=".Models.Assembly1.DataTable"  #use this as a tempory storage of the template
ex.plantsimCom.ExecuteSimTalk("%s.DisplayPanel.getElements(%s)" %(baseDisplay,template)) #set template

insp=adaptiveInspect.inspect(scInt)

insp.initTopHist()
#insp.randomCosts('gauss')
#print(insp.costs)
for n in insp.scTarget.nodes:
	insp.costs[n]=0.5
input('\n\nPlantSim Adaptive Inspection Demonstration\n\n')
ex.start()
print("Starting simulation.....")
try:
	#a=True
	#
	#	a=input("Choice:")
	#	if a=='s':
	#		ex.start()
	#		time.sleep(5)
	#		ex.stop()
	#	elif a=='r':
	#		ex.start()
	#	elif a=='0':
	#		ex.psDisconnect()
	
	while (1):
		ex.start()
		insp.analyseValue(1)
		#highest=(0,0)
		for n in insp.scTarget.nodes:
			#print(insp.values[n])
			if ex.checkNodeType(n) == "Station": #todo: evaluate more types
			#print(n)
				#print(float(ex.getVal(n,"StatRelativeOccupation")))
				ex.toggleDisplay("%s.DisplayPanel" % n,False)
				insp.values[n]=insp.values[n]*float(ex.getVal(n,"StatRelativeOccupation")*100)
				#if (insp.values[n]) > highest[0]:
				#	highest=(insp.values[n],n)
				ex.initDisplay(template,n)   #set display
		
		sol=insp.greedySearch(insp.scTarget,1)

		print("\nInspection Solution:")
		for s in sol:
			print(s[0])
		insp.executeInspection(sol)
		for s in sol:
			ex.toggleDisplay("%s.DisplayPanel" % s[0],True)
		ex.start()
		print("\nSleeping for 10 seconds...")
		print("\n\n")
		time.sleep(10)


except KeyboardInterrupt:
	ex.psDisconnect()

except Exception as e:
	print(e)
	ex.psDisconnect()



#print(ex.plantsimCom.GetValue(".Models.Assembly1.DataTable[1,1]")) # arrays start from 1 wtf




