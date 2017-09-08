from sqlalchemy import *

db = create_engine('sqlite:///midiosc.db')

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

config = Table('config', metadata,
            Column('conf_id', Integer, primary_key=True),
            Column('dawName', String(40)),
            Column('ip', Integer),
            Column('port', String),
        )

controllerState = Table('controller_state', metadata,
            Column('state_id', Integer, primary_key=True),
            # 'gain' or 'pan'
            Column('knob_mode', String(40)),  
            # 'level' or '???'
            Column('fader_mode', String(40)),
            # 0: normal, 1: send_mode on
            Column('send_mode', Integer),
            # 'solomute' or 'selectrec'
            Column('buttons_mode', Integer),
            # current bank
            Column('bank', Integer)
        )


config.create()
controllerState.create()


#default data
confI = config.insert()
confI.execute(conf_id=1, dawName='ardour', ip='127.0.0.1', port='8000')

stateI = controllerState.insert()
stateI.execute(state_id=1, knob_mode='pan', fader_mode='level', send_mode=0, buttons_mode='solomute')


