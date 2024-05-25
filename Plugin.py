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

def summonTradeHorse(s = 1):
	name = get_character_data()['name']
	inventory = get_inventory()
	items = inventory['items']
	for slot, item in enumerate(items):
		if item:
			if item['name'] == 'Donkey' or item['name'] == 'African elephant' or 'Goldclad Trade Horse' in item['name']:
				log('Summoning: '+ item['name'])
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0xEC)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				break
	return False

def HayMerca(drops):
	response = False
	if drops:
		for dropID in drops:
			if 'TRADE' in drops[dropID]['servername']:
				return True
	return False

def loop():
	stop_trace()
	stop_bot()
	drops = get_drops()
	if drops:
		for dropID in drops:
			if 'TRADE' in drops[dropID]['servername']:
				if thereIsATransport():
					x1 = get_position()['x']
					y1 = get_position()['y']
					max_distance = 0
					for dropID in drops:
						if 'TRADE' in drops[dropID]['servername']:
							x2 = drops[dropID]['x']
							y2 = drops[dropID]['y']
							dis = ((x2-x1)**2+(y2-y1)**2)**1/2
							if max_distance == 0:
								max_distance = dis
								dropID_MAS_CERCANO = dropID
							elif dis < max_distance:
								max_distance = dis
								dropID_MAS_CERCANO = dropID
					packet = b'\x01\x02\x01' + struct.pack('I', dropID_MAS_CERCANO)
					inject_joymax(0x7074, packet, False)
					log('Agarrando...')
					if notFull() and HayMerca(drops):
						Timer(0.5, loop).start()
					else:
						useBanditScroll()
				else:
					summonTradeHorse()
					Timer(0.5, loop).start()
				break
	elif not notFull():
		useBanditScroll()

def notFull():
	response = False
	pets = get_pets()
	if pets:
		for petID in pets:
			if pets[petID]['type'] == 'transport':
				for item in pets[petID]['items']:
					if item == None:
						response = True
						break
	return response

def thereIsATransport():
	bol = False
	pets = get_pets()
	if pets:
		for petID in pets:
			if pets[petID]['type'] == 'transport':
				bol = True
			elif pets[petID]['type'] == 'horse':
				DismountHorse()
	return bol

def useBanditScroll():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if x['name'] == 'Bandit Den Return Scroll':
				Packet = bytearray()
				Packet.append(i) # Inventory slot
				Packet.append(0xEC) # Always constant = 0x0C30
				Packet.append(0x09)
				inject_joymax(0x704C, Packet, True)
				log('Bandit Den Return Scroll')
		i+=1
def handle_silkroad(opcode,data):
	if opcode == 0x3091 and data ==  b'\x01':
		loop()
	return True




log("[Super Plugin v1.0 by Rahim]")