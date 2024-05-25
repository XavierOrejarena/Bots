from phBot import *
import phBotChat
import QtBind

gui = QtBind.init(__name__,'Super Plugin')
UniqueAlert = False
DesmontarPet = False
goToUnique = False
startBotUnique  = False
UniqueCheck = QtBind.createCheckBox(gui,'UniqueCh','Party chat notify',10,30)
UniqueCheck = QtBind.createCheckBox(gui,'UniqueCh','Alarm when unique is near by',10,50)
UniqueCheck = QtBind.createCheckBox(gui,'UniqueCh','Dismount',10,70)
UniqueCheck = QtBind.createCheckBox(gui,'UniqueCh','Go To Unique',10,90)
UniqueCheck = QtBind.createCheckBox(gui,'UniqueCh','Start Bot',10,110)
QtBind.setChecked(gui, UniqueCheck, UniqueAlert)

def handle_event(t, data):
	global partyAlert
	if t == 0 and UniqueAlert and '(INT)' not in data:
		DismountHorse()
		play_wav('Sounds/Unique In Range.wav')
		goUnique()
		Timer(1,goUnique).start()
		Timer(2,goUnique).start()
		if partyAlert:
			phBotChat.Party('Here ---> ['+ data + ']')

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