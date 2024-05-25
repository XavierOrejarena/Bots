from phBot import *
import phBotChat
import QtBind
from threading import Timer

gui = QtBind.init(__name__,'Super Plugin')

partyAlert = True
alarma = True
DesmontarPet = True
goToUnique = True
startBotUnique  = True

partyCheck = QtBind.createCheckBox(gui,'checkParty','Party chat notify',10,10)
alarmCheck = QtBind.createCheckBox(gui,'checkAlarm','Alarm when unique is near by',10,30)
dismountCheck = QtBind.createCheckBox(gui,'checkDismount','Dismount Pet',10,50)
gotoCheck = QtBind.createCheckBox(gui,'checkGoTo','Go To Unique',10,70)
startbotCheck = QtBind.createCheckBox(gui,'checkStartBot','Start Bot',10,90)

QtBind.setChecked(gui, partyCheck, partyAlert)
QtBind.setChecked(gui, alarmCheck, alarma)
QtBind.setChecked(gui, dismountCheck, DesmontarPet)
QtBind.setChecked(gui, gotoCheck, goToUnique)
QtBind.setChecked(gui, startbotCheck, startBotUnique)

def checkParty(checked):
	global partyAlert
	partyAlert = checked

def checkAlarm(checked):
	global alarma
	alarma = checked

def checkDismount(checked):
	global DesmontarPet
	DesmontarPet = checked

def checkGoTo(checked):
	global goToUnique
	goToUnique = checked

def checkStartBot(checked):
	global startBotUnique
	startBotUnique = checked

def handle_event(t, data):
	global partyAlert
	global alarma
	global DesmontarPet
	global goToUnique
	global startBotUnique
	if t == 0:
		if partyAlert:
			phBotChat.Party('Here ---> ['+ data + ']')
		if alarma:
			play_wav('Sounds/Unique In Range.wav')
		if DesmontarPet:
			DismountHorse()
		if goToUnique:
			goUnique()
			Timer(1,goUnique).start()
			Timer(2,goUnique).start()
		if startBotUnique:
			mobs = get_monsters()
			for mobID in mobs:
				if mobs[mobID]['type'] == 24:
					set_training_position(0, mobs[mobID]['x'],mobs[mobID]['y'],0)
					start_bot()

def DismountHorse():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			log(v['type'])
			if v['type'] == 'horse' or v['type'] == 'wolf':
				p = b'\x00'
				p += struct.pack('I', k)
				inject_joymax(0x70CB, p, False)
				log('Dismounted')
				return True
	return False

def goUnique():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['mounted'] and v['type'] == 'wolf':
				log(v['type'])
				p = b'\x00'
				p += struct.pack('I', k)
				inject_joymax(0x70CB, p, False)
				log('Dismounted')
				break
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['type'] == 24:
			move_to(mobs[mobID]['x'],mobs[mobID]['y'],0)
			return






log("[Super Plugin v1.0 by Rahim]")