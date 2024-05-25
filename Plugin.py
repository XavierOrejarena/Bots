from phBot import *
import phBotChat
import QtBind
from threading import Timer

gui = QtBind.init(__name__,'Super Plugin')
DesmontarPet = True
dismountCheck = QtBind.createCheckBox(gui,'checkDismount','Dismount Pet',10,50)
QtBind.setChecked(gui, dismountCheck, DesmontarPet)

def checkDismount(checked):
	global DesmontarPet
	DesmontarPet = checked

def handle_event(t, data):
	global DesmontarPet
	if t == 0:
		if DesmontarPet:
			DismountHorse()

def DismountHorse():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			log(v['type'])
			if v['type'] == 'horse' or v['type'] == 'wolf':
				p = b'\x00'
				p += struct.pack('I', k)
				inject_joymax(0x70CB, p, False)
				log('dismounted')
				return True
	return False

log("[Super Plugin v1.0 by Rahim]")