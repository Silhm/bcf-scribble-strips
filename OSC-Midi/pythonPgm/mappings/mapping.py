import json



class ControllerConfig:
 
    def __init__(self, controllerName):
        # Get the Controller MIDI configuration
        with open('mappings/controllers/'+controllerName+'.json', 'r') as f:
            self.ctrlConfig = json.load(f)

    #Fader block
    def getFaderNotes(self):
        return self.ctrlConfig["fader"]["touch"]["notes"]

    def getButtonNotes(self, line):
        return self.ctrlConfig["buttons"][line]["notes"]

    def getfButtonNote(self,fname):
        return self.ctrlConfig["fbuttons"][fname]
    
    def getfButtonNotes(self):
        allB = []
        fButtons = self.ctrlConfig["fbuttons"]
        fButtonsName = sorted(self.ctrlConfig["fbuttons"])
        for fb in fButtonsName:
            allB.append(fButtons[fb]["note"])
        return allB
 
    def getBankButtonNotes(self):
        up = self.ctrlConfig["bank"]["up"]["note"]
        down = self.ctrlConfig["bank"]["down"]["note"]
        return [down,up]
         
    def getVpotButtonNotes(self):
        return self.ctrlConfig["vPot"]["switch"]["notes"]

    



class DawConfig:
 
    def __init__(self, dawName):
        # Get the DAW OSC configuration
        with open('mappings/daw-osc/'+dawName+'.json', 'r') as f:
            self.dawConfig = json.load(f)


    def getFaderAddress(self):
        return self.dawConfig["strip"]["fader"]["address"]


    def getButtonAddress(self, line, controllerButtonMode):
        if line == 1:
            return self.dawConfig["strip"]["solo" if controllerButtonMode == "solomute" else "select"]["address"]
        elif line == 2:
            return self.dawConfig["strip"]["mute" if controllerButtonMode == "solomute" else "rec"]["address"]


    def getButtonValue(self, line, controllerButtonMode, on):
        val = "valueOn" if on else "valueOff"
        if line == 1:
            return self.dawConfig["strip"]["solo" if controllerButtonMode == "solomute" else "select"][val]
        elif line == 2:
            return self.dawConfig["strip"]["mute" if controllerButtonMode == "solomute" else "rec"][val]


    def getFunctionAddress(self, fname):
        return self.dawConfig["function"][fname]


    def getVpotAddress(self, controllerVpotMode):
        return self.dawConfig["strip"]["panStereoPosition" if controllerVpotMode == "pan" else "gain"]["address"]



