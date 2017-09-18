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
    
    def _createNewStrip(self, sId):
        dbStrip = self.db.dawStrip.find_one({'id':sId})
        strip = self._defaultStrip.copy()
        strip["id"] = sId
        strip["name"] = "track {}".format(sId)

        if(dbStrip):
            return dbStrip
        else:
            self.db.dawStrip.insert_one(strip)
            return strip




    def getDawIpAddress(self, dawName='ardour'):
        return self.db.dawConfig.find_one({'dawName':dawName})["ip"]

    def getDawPort(self, dawName='ardour'):
        return self.db.dawConfig.find_one({'dawName':dawName})["port"]

    def getButtonMode(self):
        return self.db.controllerState.find_one()["buttons_mode"]

    def getVpotMode(self):
        return self.db.controllerState.find_one()["vpot_mode"]

    def setButtonMode(self, mode):
        """
        Set the button Mode: "solomute" or "selectrec"
        """
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
        """
        Save the last known fader Position for a given track
        """
        strip = self.db.dawStrip.find_one( { "id": faderId } )
        if not strip:
            newStrip = self._defaultStrip
            newStrip["id"] = faderId
            newStrip["name"] = "track {}".format(faderId)
            newStrip["fader"] = faderPos
            
            self.db.dawStrip.insert_one(newStrip)
        else:
            self.db.dawSession.find_one_and_update( { "id": faderId }, {'$set': { "fader" : faderPos}} )    
 
 
    def setPanPosition(self, knobId, panPos):
        """
        Save the last known pan Position for a given track
        """
        strip = self.db.dawStrip.find_one( { "id": knobId } )
        if not strip:
            newStrip = self._defaultStrip
            newStrip["id"] = knobId
            newStrip["name"] = "track {}".format(knobId)
            newStrip["pan"] = panPos
            
            self.db.dawStrip.insert_one(newStrip)
        else:
            self.db.dawSession.find_one_and_update( { "id": knobId }, {'$set': { "pan" : panPos}} )    


    def setGainPosition(self, knobId, gainPos):
        """
        Save the last known gain Position for a given track
        """
        strip = self.db.dawStrip.find_one( { "id": knobId } )
        if not strip:
            newStrip = self._defaultStrip
            newStrip["id"] = knobId
            newStrip["name"] = "track {}".format(knobId)
            newStrip["pan"] = gainPos
            
            self.db.dawStrip.insert_one(newStrip)
        else:
            self.db.dawSession.find_one_and_update( { "id": faderId }, {'$set': { "pan" : gainPos}} )    


    def getButtonState(self, line, bId, buttonMode):
        """
        Get the button State according to params
        """
        param = "select"
        if line == 1:
            param = "solo" if buttonMode == "solomute" else "select"
        elif line == 2:
            param = "mute" if buttonMode == "solomute" else "rec"

        strip = self.db.dawStrip.find_one( {"id" : bId} )
        
        if not strip:
            strip = self._defaultStrip
            strip["id"] = bId
            strip["name"] = "track {}".format(bId)

            self.db.dawStrip.insert_one(strip)
            
        return bool(strip[param])


    def setButtonState(self, line, bId, buttonMode, value):
        """
        Set the button State according to params
        """
        param = "select"
        if line == 1:
            param = "solo" if buttonMode == "solomute" else "select"
        elif line == 2:
            param = "mute" if buttonMode == "solomute" else "rec"

        strip = self.db.dawStrip.find_one( {"id" : bId} )
        if not strip:
            strip = self._createNewStrip(bId)
        
        self.db.dawStrip.find_one_and_update( { "id": bId }, {'$set': { param : bool(value)}} )



    def getvPotValue(self, vPotId, vPotMode):
        """
        Get the vPot in db according to mode
        """
        strip = self.db.dawStrip.find_one( {"id" : vPotId} )
        if not strip:
            strip = self._createNewStrip(vPotId)

        return strip[vPotMode]


    def setvPotValue(self, vPotId, vPotMode, value):
        """
        Set the vPot in db according to mode
        """
        strip = self.db.dawStrip.find_one( {"id" : vPotId} )
        if not strip:
            strip = self._createNewStrip(vPotId)

        self.db.dawStrip.find_one_and_update( { "id": vPotId }, {'$set': { vPotMode : value}} )

