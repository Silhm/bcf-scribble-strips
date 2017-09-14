from pymongo import MongoClient


class Database:
    def __init__(self):

        client = MongoClient()
        self.db = client.midiosc

    def getButtonMode(self):
        return self.db.controllerState.find_one()["buttons_mode"]

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

