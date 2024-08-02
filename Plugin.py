from phBot import *
import struct
import phBotChat
import QtBind
from threading import Timer
import urllib.request
import ssl
import threading

gui = QtBind.init(__name__,'Super Plugin')

uniqueList = []
partyAlert = True
alarma = True
DesmontarPet = True
goToUnique = True
startBotUnique  = False
TelegramBol = False
UniqueTelegram = False
partyNumber = ''
comandos = False
spawn = False

partyCheck = QtBind.createCheckBox(gui,'checkParty','Party chat notify',10,10)
alarmCheck = QtBind.createCheckBox(gui,'checkAlarm','Alarm when unique is near by',10,30)
dismountCheck = QtBind.createCheckBox(gui,'checkDismount','Dismount Pet',10,50)
gotoCheck = QtBind.createCheckBox(gui,'checkGoTo','Go To Unique',10,70)
startbotCheck = QtBind.createCheckBox(gui,'checkStartBot','Start Bot',10,90)
telegramCheck = QtBind.createCheckBox(gui,'checkTelegram','Telegram PM',10,110)
uniqueCheck = QtBind.createCheckBox(gui,'checkUnique','Telegram Unique',10,130)
comandosCheck = QtBind.createCheckBox(gui,'checkComandos','Chat Commands',10,150)
spawnCheck = QtBind.createCheckBox(gui,'checkSpawn','Spawn Alarm',10,170)
TelegramID = QtBind.createLineEdit(gui,"",650,276,70,20)
TelegramBot = QtBind.createLineEdit(gui,"https://t.me/The_Silkroad_bot",20,276,160,20)
TelegramLabel = QtBind.createLabel(gui,'Telegram ID:',587,280)

lstOpcodes = QtBind.createList(gui,621,30,100,80)
btnRemOpcode = QtBind.createButton(gui,'removeIgnore',"     GO & BOT     ",635,113)
btnAddOpcode = QtBind.createButton(gui,'llenarLista',"      REFRESH      ",630,10)

lblOpcodes = QtBind.createLabel(gui,"Unique List",321,110)
tbxOpcodes = QtBind.createLineEdit(gui,"",321,129,100,20)
lstOpcodes = QtBind.createList(gui,321,151,176,109)
btnAddOpcode = QtBind.createButton(gui,'addUnique',"      Add      ",423,129)
btnRemOpcode = QtBind.createButton(gui,'removeUnique',"     Remove     ",370,259)

def addUnique():
	ignored = QtBind.text(gui,tbxOpcodes).lower()
	if ignored not in uniqueList:
		uniqueList.append(ignored)
		QtBind.append(gui,lstOpcodes,ignored)
	else:
		log('repetidoooo!!!')

def removeUnique():
	selectedItem = QtBind.text(gui,lstOpcodes)
	if selectedItem:
		QtBind.remove(gui,lstOpcodes,selectedItem)
		uniqueList.remove(selectedItem)

QtBind.setChecked(gui, partyCheck, partyAlert)
QtBind.setChecked(gui, alarmCheck, alarma)
QtBind.setChecked(gui, dismountCheck, DesmontarPet)
QtBind.setChecked(gui, gotoCheck, goToUnique)
QtBind.setChecked(gui, startbotCheck, startBotUnique)
QtBind.setChecked(gui, telegramCheck, TelegramBol)
QtBind.setChecked(gui, comandosCheck, comandos)
QtBind.setChecked(gui, spawnCheck, spawn)

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

def checkTelegram(checked):
	global TelegramBol
	TelegramBol = checked

def checkUnique(checked):
	global UniqueTelegram
	UniqueTelegram = checked

def checkComandos(checked):
	global comandos
	comandos = checked

def checkSpawn(checked):
	global spawn
	spawn = checked

def llenarLista():
	QtBind.clear(gui,lstOpcodes)
	Party = get_party()
	if Party:
		for memberID in Party:
			if Party[memberID]['name'] != get_character_data()['name']:
				QtBind.append(gui,lstOpcodes,Party[memberID]['name'])

def removeIgnore():
	selectedItem = QtBind.text(gui,lstOpcodes)
	if selectedItem:
		Party = get_party()
		if Party:
			for memberID in Party:
				if selectedItem == Party[memberID]['name']:
					set_training_position(Party[memberID]['region'], Party[memberID]['x'], Party[memberID]['y'], 0.0)
					start_bot()

def handle_event(t, data):
	global partyAlert
	global spawn
	global DesmontarPet
	global goToUnique
	global startBotUnique
	if t == 0:
		if partyAlert:
			phBotChat.Party('Here ---> ['+ data + ']')
		if spawn:
			play_wav('Sounds/Unique In Range.wav')
		if DesmontarPet:
			DismountHorse()
		if goToUnique:
			goUnique()
			Timer(1,goUnique).start()
			Timer(2,goUnique).start()
		if startBotUnique:
			Timer(2,startUnique).start()

def startUnique():
	log('el bot iniciara en 1 segundo')
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
				log('dismounted')
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

def joinParty(n):
	global partyNumber
	if not get_party() and n != 0:
		Packet = bytearray()
		Packet += struct.pack('<I', n)
		inject_joymax(0x706D, Packet, False)
		Timer(5,joinParty,[n]).start()

def spawnHorse():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if '_C_DHORSE' in x['servername']:
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0xEC)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				break
		i+=1

def handle_silkroad(opcode,data):
	global partyNumber
	if opcode == 0x3091 and data ==  b'\x00':
		joinParty(partyNumber)
		return False
	elif opcode == 0x706D:
		partyNumber = struct.unpack_from('<I', data, 0)[0]
		notice(str(partyNumber))
	return True


def handle_chat(t,player,msg):
	global TelegramBol
	global partyNumber
	global comandos
	if t == 2:
		if TelegramBol:
			threading.Thread(target=sendTelegram, args=[player + " -> " + get_character_data()['name'] + ' -> ' + msg],).start()
		foo = msg.split()
		for word in foo:
			if word.isnumeric():
				notice(word)
				partyNumber = int(word)
				break
	if msg == 'stop':
		partyNumber == 0
	if comandos:
		if msg == 'stop':
			stop_trace()
			stop_bot()
		elif msg == 'follow':
			stop_bot()
			stop_trace()
			if get_character_data()['name'] != player:
				start_trace(player)
		elif msg == 'start':
			stop_trace()
			start_bot()
		elif (t == 2 or t == 1 or t == 4) and msg[0:2] == '>>' and msg[3] != ' ':
			stop_trace()
			stop_bot()
			log(get_config_dir().replace('Config','Scripts')+msg[2:]+'.txt')
			set_training_script(get_config_dir().replace('Config','Scripts')+msg[2:]+'.txt')
			start_bot()
		elif msg.lower() == 'here' and get_character_data()['name'] == player:
			stop_bot()
			stop_trace()
			set_training_position(0, get_character_data()['x'], get_character_data()['y'], 0)
			start_bot()
		elif (t == 1 or t == 2 or t == 4) and msg[0] == 'r' and msg[1:].isnumeric() and len(msg[1:]) < 4:
			r = float(msg[1:len(msg)])
			set_training_radius(r)
		elif msg == 'spawnhorse':
			spawnHorse()
		elif msg.lower() == 'leave':
			inject_joymax(0x7061, bytearray(), False)


def handle_joymax(opcode, data):
	global UniqueTelegram
	global uniqueList
	global alarma
	if opcode == 0x3864 and data:
		if struct.unpack_from('<s', data, 0)[0] == b'\x02':
			name = struct.unpack_from('<' + str(data[6]) + 's',data,8)[0].decode('cp1252')
			mobs = get_monsters()
			for mobID in mobs:
				if mobs[mobID]['type'] == 24:
					phBotChat.Party(name + ' Here! => ['+mobs[mobID]['name'] +']')
					break
	elif opcode == 0x300C and data[0] == 5: # Unique Spawn 
			uniqueName = get_monster(struct.unpack_from('<I', data, 2)[0])['name']
			log(uniqueName)
			for unique in uniqueList:
				if unique in uniqueName.lower() :
					if spawn:
						play_wav('Sounds/Unique.wav')
					if UniqueTelegram:
						threading.Thread(target=sendTelegram, args=[uniqueName],).start()
					return True
	return True

def sendTelegram(data):
	log(data)
	id = QtBind.text(gui,TelegramID)
	url = 'https://api.telegram.org/bot6863881576:AAFjOYMaXdH_K_OBUnuDGaKNfJFkOQfoMgc/sendMessage?chat_id='+id+'&parse_mode=Markdown&text='
	if '_' in data:
		url = 'https://api.telegram.org/bot6863881576:AAFjOYMaXdH_K_OBUnuDGaKNfJFkOQfoMgc/sendMessage?chat_id='+id+'&text='
	url = url + urllib.parse.quote(data)
	urllib.request.urlopen(url,context=ssl._create_unverified_context())

def notice(message):
	p = struct.pack('B',7)
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x3026,p,False)

log("[Super Plugin v2.0 by Rahim]")
