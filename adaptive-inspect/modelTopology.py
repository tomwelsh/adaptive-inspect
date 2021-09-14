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
            self.scInterface=modelSC.SupplyChainInterface()
        else:
            if type(sc) == 'SupplyChain':
                self.scInterface=scInterface
            else:
                raise Exception("Not a SC Object")
        self.scInterface.setAssetModel(self.assetModel)

    def genRandom(self,params=5):
        self.scInterface.randomSC(params)
