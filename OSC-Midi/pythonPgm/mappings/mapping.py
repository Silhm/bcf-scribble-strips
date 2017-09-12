import json



class ControllerConfig:
 
    def __init__(self, controllerName):
        # Get the Controller MIDI configuration
        with open('mappings/controllers/'+controllerName+'.json', 'r') as f:
            self.ctrlConfig = json.load(f)

    def getFaderNotes(self):
        return self.ctrlConfig["fader"]["touch"]["notes"]

    def getButtonNotes(self, line):
        return self.ctrlConfig["buttons"][line]["notes"]


class DawConfig:
 
    def __init__(self, dawName):
        # Get the DAW OSC configuration
        with open('mappings/daw-osc/'+dawName+'.json', 'r') as f:
            self.dawConfig = json.load(f)

