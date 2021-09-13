import modelSC
import modelAsset


class scTopology:

    def __init__(self,sc=None,asset=None):


        #if asset==None:
        self.assetModel=modelAsset
        #else:
        #    if type(asset)=='asset':
        #        self.assetModel=modelAsset
        #    else:
        #        raise Exception("Not an asset object")

        if sc==None:
            self.sc=modelSC.SupplyChain()
        else:
            if type(sc) == 'SupplyChain':
                self.sc=sc
            else:
                raise Exception("Not a SC Object")
        self.sc.setAssetModel(self.assetModel)

    def genRandom(self,params=5):
        self.sc.randomSC(params)
