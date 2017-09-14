from pymongo import MongoClient
client = MongoClient()
db = client.midiosc

print("=== This will drop all configuration an make a factory reset ===")

daw = input('Enter the daw used: (default is Ardour) ')
daw = daw if daw else "ardour"

controller = input('Enter the controller: (default is BCF2000) ')
controller = controller if controller else "bcf2000"

ctrlNumber = input('How many?: (default is 1) ')
ctrlNumber = ctrlNumber if ctrlNumber else 1


client.drop_database(db)


# Daw
dawConfig = db.dawConfig

defaultDawConfig = {
        "dawName": "ardour",
        "ip": "127.0.0.1",
        "port": 3128
        }

dawConfig.insert_one(defaultDawConfig)


# Controller
controllerConfig = db.controllerConfig

defaultControllerConfig = {
        "controllerName": "bcf2000",
        "bankSize": 8,
        "count": 1
}
controllerConfig.insert_one(defaultControllerConfig)

# Controller state
controllerState = db.controllerState

defaultControllerState = {
            # 'gain' or 'pan'
            "vpot_mode" : "pan",
            # 'level' or '???'
            "fader_mode" : "level",
            # 'solomute' or 'selectrec'
            "buttons_mode" : "solomute",
            # current bank
            "bank" : 0
}
controllerState.insert_one(defaultControllerState)

# DAW Session
dawSession = db.dawSession

defaultDawSession = {
        "sessionName": "default Session",
        "strips" : [
            {
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
         ],
        "master" : {
            "fader" : 0,
            "gain": 0,
            "pan": 0.5,
            "mute": False,
         },
        "transport": {
            "play": False,
            "recArm": False,
            "loop": False
        }
}

dawSession.insert_one(defaultDawSession)

