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
		for slot, pet in pets.items():
			if pet['type'] == 'horse' or pet['type'] == 'wolf':
				log('yes')
				p = b'\x00'
				p += struct.pack('I', slot)
				inject_joymax(0x70CB, p, False)
				log('dismounted')
				return True

log("[Super Plugin v1.0 by Rahim]")