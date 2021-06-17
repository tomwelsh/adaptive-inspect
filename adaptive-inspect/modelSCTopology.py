import modelSC
import modelAsset


class scTopology:

    def __init__(self,sc=None,asset=None):

        if sc=None:
            self.sc=modelSC.SupplyChain()
        else:
            if type(sc) == 'SupplyChain':
                self.sc=sc
            else:
                raise Exception("Not a SC Object")

        if asset=None:
            self.asset=modelAsset()
        else:
            if type(asset)='asset'
                self.asset=asset
            else:
                raise Exception("Not an asset object")


    def genRandom(self,params=5):
        self.sc.randomSC(params)
