from pymongo import MongoClient


class Database:
    def __init__(self):

        client = MongoClient()
        self.db = client.midiosc

        self._defaultStrip = {
            "id": 1,
            "name": "track 1",
            "fader" : 0,
            "gain": 0,
            "pan": 0.5,
            "mute": False,
            "solo": False,
            "rec": False,
            "select": True,
            "polarity": False
        }
    




    def getDawIpAddress(self, dawName='ardour'):
        return self.db.dawConfig.find_one({'dawName':dawName})["ip"]

    def getDawPort(self, dawName='ardour'):
        return self.db.dawConfig.find_one({'dawName':dawName})["port"]

    def getButtonMode(self):
        return self.db.controllerState.find_one()["buttons_mode"]

    def getVpotMode(self):
        return self.db.controllerState.find_one()["vpot_mode"]

    def setButtonMode(self, mode):
        self.db.controllerState.find_one_and_update( {}, {'$set': {'buttons_mode': mode}} )


    def getDawName(self):
        return self.db.dawConfig.find_one()["dawName"]

    def getControllerName(self):
        return self.db.controllerConfig.find_one()["controllerName"]


    def getBankSize(self):
        return self.db.controllerConfig.find_one()["bankSize"]

    def getCurrentBank(self):
        return self.db.controllerState.find_one()["bank"]

    
    def bankUp(self):
        self.db.controllerState.find_one_and_update( {}, {'$inc': {'bank': 1}} )

    def bankDown(self):
        self.db.controllerState.find_one_and_update( {}, {'$inc': {'bank': -1}} )

    def setFaderPosition(self, faderId, faderPos):
        stripKey = "strips.{}.id".format(faderId)
        stripFaderKey = "strips.{}.fader".format(faderId)

        strip = self.db.dawSession.find_one( { stripKey: faderId } )
        if not strip:
            newStrip = self._defaultStrip
            newStrip["id"] = faderId
            newStrip["name"] = "track {}".format(faderId)
            key = "strips.{}".format(faderId)
            
            self.db.dawSession.find_one_and_update( {}, {'$set': { key : newStrip } } )

        self.db.dawSession.find_one_and_update( { stripKey: faderId }, {'$set': { stripFaderKey : faderPos}} )    

