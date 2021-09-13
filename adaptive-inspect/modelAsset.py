

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
		#self.modelTopology=modelTopology
		self.name=name
		self.assetType=assetType #0=physical, 1=cyber, 2=human
		self.minCost=minCost #intrusiveness
		self.value=value
		self.states=[]

	def function(self):
		#override with process function
		return 0

	def randomAsset(self,size):
		for i in range(size):
			self.states.append(random.randint(100))
