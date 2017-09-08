"""
Display lib
"""

DISPLAY_COUNT = 16


class Display:
    def __init__(self, type):
        self.type = type
        self.strips = {}
        

    def _newStrip(self,sId):
        return {
            id : sId,
            name: 'strip '+sId,
            level: 0,
            fader: 0,
            gain: 0 ,
            mute: false,
            solo: false,
            rec: false,
            polarity: false,
            panStereoPosition: 0.5,
            select: false
        }


    def stripName(self, sId, sName):    
        """
        Display the name of a strip by ID
        """
        #Create it if doesn't exists
        if not sId in self.strips:
            self.strips[sID] = self._newStrip(self,sId)

        self.strips[sID].name = sName 
        

    def stripMute(self, sId, mute):
        """
        Set the mute state of strip by ID
        """
        #Create it if doesn't exists
        if not sId in self.strips:
            self.strips[sID] = self._newStrip(self,sId)

