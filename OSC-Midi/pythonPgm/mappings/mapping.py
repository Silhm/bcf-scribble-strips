import json



class ControllerConfig:
 
    def __init__(self, controllerName):
        # Get the Controller MIDI configuration
        with open('mappings/controllers/'+controllerName+'.json', 'r') as f:
            self.ctrlConfig = json.load(f)

    #Fader block
    def getFaderNotes(self):
        return self.ctrlConfig["fader"]["touch"]["notes"]

    def getFaderMove(self, k):
        return self.ctrlConfig["fader"]["move"][k]

    def getButtonNotes(self, line):
        return self.ctrlConfig["buttons"]["line{}".format(line)]["notes"]
    
    def getButtonType(self, line):
        return self.ctrlConfig["buttons"]["line{}".format(line)]["type"]

    def getfButtonNote(self,fname):
        return self.ctrlConfig["fbuttons"][fname]
    
    def getfButtonNotes(self):
        allB = []
        fButtons = self.ctrlConfig["fbuttons"]
        fButtonsName = sorted(self.ctrlConfig["fbuttons"])
        for fb in fButtonsName:
            allB.append(fButtons[fb]["note"])
        return allB
    
    def getfButtonNote(self, fButtonName, type):
        return self.ctrlConfig["fbuttons"][fButtonName][type]

 
    def getBankButtonNotes(self):
        up = self.ctrlConfig["bank"]["up"]["note"]
        down = self.ctrlConfig["bank"]["down"]["note"]
        return [down,up]
         
    def getVpotButtonNotes(self):
        return self.ctrlConfig["vPot"]["switch"]["notes"]

    def getVpotCC(self):
        return self.ctrlConfig["vPot"]["pot"]["CC"]
    
    def getVpotRotation(self, val):
        rotations = self.ctrlConfig["vPot"]["pot"]["rotation"]
        
        CW  = rotations["CW"]
        CCW = rotations["CCW"]

        direction = "CW"

        if val < CW + 5:
            speed = val - (CW-1) 
            direction = "CW"
        else:
            speed = val - (CCW-1)
            direction = "CCW"

        return (direction, speed)

    def getFaderMidiRange(self):
        return self.ctrlConfig["fader"]["move"]["valueRange"]



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


    def getFunctionAddress(self, fname=False):
        if(fname):
            return self.dawConfig["function"][fname]
        else:
            return self.dawConfig["function"]


    def getVpotAddress(self, controllerVpotMode):
        return self.dawConfig["strip"]["panStereoPosition" if controllerVpotMode == "pan" else "gain"]["address"]

    def getFaderOSCRange(self):
        return self.dawConfig["strip"]["fader"]["valueRange"]

