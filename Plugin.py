from phBot import *
import struct
import phBotChat
import QtBind
from threading import Timer
import urllib.request
import ssl
import threading
import json
import os.path
 
gui = QtBind.init(__name__,'Super Plugin')
partyAlert = True
alarma = True
DesmontarPet = True
goToUnique = True
startBotUnique  = False
TelegramBol = False
UniqueTelegram = False
comandos = False
spawn = False
uniqueList = ['str','int']
idTelegram = ''
unionNotify = False
alertar_hunter = False
count = False

def loadConfig():
	global partyAlert
	global alarma
	global DesmontarPet
	global goToUnique
	global startBotUnique 
	global TelegramBol
	global UniqueTelegram
	global comandos
	global spawn
	global uniqueList
	global idTelegram
	global unionNotify
	global alertar_hunter
	global count
	if os.path.isfile('sample.json'):
		with open('sample.json', 'r') as openfile:
			json_object = json.load(openfile)
			partyAlert = json_object['partyAlert']
			alarma = json_object['alarma']
			DesmontarPet = json_object['DesmontarPet']
			goToUnique = json_object['goToUnique']
			startBotUnique = json_object['startBotUnique'] 
			TelegramBol = json_object['TelegramBol']
			UniqueTelegram = json_object['UniqueTelegram']
			comandos = json_object['comandos']
			spawn = json_object['spawn']
			uniqueList = json_object['uniqueList']
			idTelegram = json_object['idTelegram']
			if 'count' in json_object:
				count = json_object['count']
			if 'unionNotify' in json_object:
				unionNotify = json_object['unionNotify']
			if 'alertar_hunter' in json_object:
				alertar_hunter = json_object['alertar_hunter']
			QtBind.createLineEdit(gui,idTelegram,650,276,70,20)

loadConfig()

def saveConfig():
	global partyAlert
	global alarma
	global DesmontarPet
	global goToUnique
	global startBotUnique 
	global TelegramBol
	global UniqueTelegram
	global comandos
	global spawn
	global uniqueList
	global idTelegram
	global gui
	global unionNotify
	global alertar_hunter
	global count
	# Data to be written
	dictionary = {
	    'partyAlert': partyAlert,
		'alarma': alarma,
		'DesmontarPet': DesmontarPet,
		'goToUnique': goToUnique,
		'startBotUnique': startBotUnique,
		'TelegramBol': TelegramBol,
		'UniqueTelegram': UniqueTelegram,
		'comandos': comandos,
		'spawn': spawn,
		'uniqueList': uniqueList,
		'idTelegram': QtBind.text(gui,TelegramID),
		'unionNotify': unionNotify,
		'alertar_hunter': alertar_hunter,
		'count': count,
	}

	# Serializing json
	json_object = json.dumps(dictionary, indent=4)
	 
	# Writing to sample.json
	with open("sample.json", "w") as outfile:
	    outfile.write(json_object)

mobAtacked = []
attackWolf = False
itemListAzul = ['advanced','sharpness','lottery','silk scroll','immortal','lucky','poro','sabakun','coin','blue stone','serapis']
otrosItems = ['Reverse Reverse Return Scroll','Global chatting','Magic POP Card']
PICK = False
CountList = ['Cbum','Seven']
energy = False
pmList = []
WhiteList = ['Seven','Cbum','Kurumi','Moshi','Zoser','Fami', 'Pomi', 'Lestrange']
bolnotify = False


partyNumber = ''
perma_trace = False
follow_hunter = False
party_hunter = False
dc_hunter = False
tlg_hunter = False
start_hunter = False
alertar_thief = False
party_thief = False
dc_thief = False
tlg_thief = False
start_thief = False
merca = False
ScrollAfterZerk = False

ignoreZones = ['Samarkand','Jangan','Königreich Hotan','Western-China-Donwhang','Constantinople','Alexandria','Tempel','Flammenberg']
pm_hunter = False
bol = True
ignore = ['Rahim']

if get_character_data()['name'] in WhiteList:
	gui2 = QtBind.init(__name__,'Job Expert')
	buscarMercabtn = QtBind.createButton(gui2,'buscarMerca','buscarMerca',150,10)
	cbxSro3 = QtBind.createCheckBox(gui2,'cbxSro_clicked3','Thief Activate',10,150)
	cbxSro4 = QtBind.createCheckBox(gui2,'cbxSro_clicked4','Party Thief',30,170)
	cbxSro5 = QtBind.createCheckBox(gui2,'cbxSro_clicked5','DC Thief',30,190)
	cbxSro7 = QtBind.createCheckBox(gui2,'cbxSro_clicked7','Telegram Thief',30,210)

	lblOpcodes = QtBind.createLabel(gui2,"Ignore list ( Filter )",321,110)
	tbxOpcodes = QtBind.createLineEdit(gui2,"",321,129,100,20)
	lstOpcodes = QtBind.createList(gui2,321,151,176,109)
	btnAddOpcode = QtBind.createButton(gui2,'addIgnore',"      Add      ",423,129)
	btnRemOpcode = QtBind.createButton(gui2,'removeIgnore',"     Remove     ",370,259)

	cbxSro0 = QtBind.createCheckBox(gui2,'cbxSro_clicked0','Hunter Activate',10,10)
	cbxSro1 = QtBind.createCheckBox(gui2,'cbxSro_clicked1','Party Hunter',30,30)
	cbxSro11 = QtBind.createCheckBox(gui2,'cbxSro_clicked11','Perma Trace',30,50)
	cbxSro6 = QtBind.createCheckBox(gui2,'cbxSro_clicked6','Telegram Hunter',30,70)
	cbxSro10 = QtBind.createCheckBox(gui2,'cbxSro_clicked10','Follow Hunter',30,90)
	cbxSro8 = QtBind.createCheckBox(gui2,'cbxSro_clicked8','PM Hunter',30,110)
	QtBind.setChecked(gui2, cbxSro0, alertar_hunter)

partyCheck = QtBind.createCheckBox(gui,'checkParty','Party chat notify',10,10)
alarmCheck = QtBind.createCheckBox(gui,'checkAlarm','Alarm when unique is near by',10,30)
dismountCheck = QtBind.createCheckBox(gui,'checkDismount','Dismount Pet',10,50)
gotoCheck = QtBind.createCheckBox(gui,'checkGoTo','Go To Unique',10,70)
startbotCheck = QtBind.createCheckBox(gui,'checkStartBot','Start Bot',10,90)
telegramCheck = QtBind.createCheckBox(gui,'checkTelegram','Telegram PM',10,110)
uniqueCheck = QtBind.createCheckBox(gui,'checkUnique','Telegram Unique',10,130)
comandosCheck = QtBind.createCheckBox(gui,'checkComandos','Chat Commands',10,150)
spawnCheck = QtBind.createCheckBox(gui,'checkSpawn','Spawn Alarm',10,170)
scrollCheck = QtBind.createCheckBox(gui,'checkScroll','Scroll After Zerk',10,190)
unionCheck = QtBind.createCheckBox(gui,'checkUnion','Union Unique Drop',10,210)
countCheck = QtBind.createCheckBox(gui,'checkCount','Auto Count',10,230)
TelegramID = QtBind.createLineEdit(gui,idTelegram,650,276,70,20)
TelegramBot = QtBind.createLineEdit(gui,"https://t.me/The_Silkroad_bot",20,276,160,20)
TelegramLabel = QtBind.createLabel(gui,'Telegram ID:',587,280)

lstOpcodes = QtBind.createList(gui,621,30,100,80)
btnRemOpcode = QtBind.createButton(gui,'removeIgnore',"     GO & BOT     ",635,113)
btnAddOpcode = QtBind.createButton(gui,'llenarLista',"      REFRESH      ",630,10)

lblOpcodes = QtBind.createLabel(gui,"Unique List",321,110)
qtUniqueAdd = QtBind.createLineEdit(gui,"",321,129,100,20)
qtUniqueList = QtBind.createList(gui,321,151,176,109)
btnAddOpcode = QtBind.createButton(gui,'addUnique',"      Add      ",423,129)
btnRemOpcode = QtBind.createButton(gui,'removeUnique',"     Remove     ",370,259)

def soundMerca():
	log('Buscando...')
	global merca
	if merca:
		drops = get_drops()
		if drops:
			for dropID in drops:
				if 'TRADE' in drops[dropID]['servername']:
					log(drops[dropID]['servername'])
					stop_bot()
					merca = False
					play_wav('Sounds/MercaEncontrada.wav')
					break
		Timer(1,soundMerca).start()

def telegram(url):
	urllib.request.urlopen(url,context=ssl._create_unverified_context())
		
def Desconectar():
	inject_joymax(0x704C, bytearray(), False)
	while True:
		os.kill(os.getpid(), 9)

def addIgnore():
	ignored = QtBind.text(gui2,tbxOpcodes)
	ignore.append(ignored)
	QtBind.append(gui2,lstOpcodes,ignored)

def removeIgnore():
	selectedItem = QtBind.text(gui2,lstOpcodes)
	if selectedItem:
		QtBind.remove(gui2,lstOpcodes,selectedItem)

def addUnique():
	selectedUnique = QtBind.text(gui,qtUniqueAdd).lower()
	if selectedUnique != '' and selectedUnique not in uniqueList:
		uniqueList.append(selectedUnique)
		QtBind.append(gui,qtUniqueList,selectedUnique)
	else:
		log('repetidoooo!!!')
	saveConfig()

def removeUnique():
	selectedItem = QtBind.text(gui,qtUniqueList)
	if selectedItem:
		QtBind.remove(gui,qtUniqueList,selectedItem)
		uniqueList.remove(selectedItem)
	saveConfig()

QtBind.setChecked(gui, partyCheck, partyAlert)
QtBind.setChecked(gui, alarmCheck, alarma)
QtBind.setChecked(gui, dismountCheck, DesmontarPet)
QtBind.setChecked(gui, gotoCheck, goToUnique)
QtBind.setChecked(gui, startbotCheck, startBotUnique)
QtBind.setChecked(gui, telegramCheck, TelegramBol)
QtBind.setChecked(gui, uniqueCheck, UniqueTelegram)
QtBind.setChecked(gui, comandosCheck, comandos)
QtBind.setChecked(gui, spawnCheck, spawn)
QtBind.setChecked(gui, unionCheck, unionNotify)
QtBind.setChecked(gui, countCheck, count)

def buscarMerca():
	global merca
	merca = not merca
	soundMerca()

def cbxSro_clicked10(checked):
	global follow_hunter
	follow_hunter = checked
	stop_trace()

def cbxSro_clicked11(checked):
	global perma_trace
	perma_trace = checked
	stop_trace()

def cbxSro_clicked8(checked):
	global pm_hunter
	pm_hunter = checked

def cbxSro_clicked9(checked):
	global start_thief
	start_thief = checked

def cbxSro_clicked0(checked):
	global alertar_hunter
	alertar_hunter = checked
	saveConfig()

def cbxSro_clicked1(checked):
	global party_hunter
	party_hunter = checked

def cbxSro_clicked2(checked):
	global dc_hunter
	dc_hunter = checked

def cbxSro_clicked3(checked):
	global alertar_thief
	alertar_thief = checked

def cbxSro_clicked4(checked):
	global party_thief
	party_thief = checked

def cbxSro_clicked5(checked):
	global dc_thief
	dc_thief = checked

def cbxSro_clicked6(checked):
	global tlg_hunter
	tlg_hunter = checked

def cbxSro_clicked7(checked):
	global tlg_thief
	tlg_thief = checked

def checkParty(checked):
	global partyAlert
	partyAlert = checked
	saveConfig()

def checkAlarm(checked):
	global alarma
	alarma = checked
	saveConfig()

def checkDismount(checked):
	global DesmontarPet
	DesmontarPet = checked
	saveConfig()

def checkGoTo(checked):
	global goToUnique
	goToUnique = checked
	saveConfig()

def checkStartBot(checked):
	global startBotUnique
	startBotUnique = checked
	saveConfig()

def checkTelegram(checked):
	global TelegramBol
	TelegramBol = checked
	saveConfig()

def checkUnique(checked):
	global UniqueTelegram
	UniqueTelegram = checked
	saveConfig()

def checkComandos(checked):
	global comandos
	comandos = checked
	saveConfig()

def checkSpawn(checked):
	global spawn
	spawn = checked
	saveConfig()

def checkScroll(checked):
	global ScrollAfterZerk
	ScrollAfterZerk = checked

def checkUnion(checked):
	global unionNotify
	unionNotify = checked
	saveConfig()

def checkCount(checked):
	global count
	count = checked
	saveConfig()

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
	global party_hunter
	global party_thief
	global dc_hunter
	global dc_thief
	global start_hunter
	global start_thief
	global follow_hunter
	global perma_trace
	global pmList
	global bolnotify
	if t == 0:
		bolnotify = True
		notice(data)
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
	if get_character_data()['name'] in WhiteList:
		if t == 1 and data not in QtBind.getItems(gui2,lstOpcodes) and data not in ignore:
			log('[HUNTER] '+data)
			if alertar_hunter:
				play_wav('Sounds/Hunter.wav')
				checkThief(0)
				notice(data)
			if dc_hunter:
				Desconectar()
			if party_hunter and get_inventory()['items'][8] and get_zone_name(get_position()['region']) not in ignoreZones and data not in pmList:
				pmList.append(data)
				phBotChat.Party("HUNTER: [" + data  + "]")
			if tlg_hunter:
				name = get_character_data()['name']
				# url = 'https://api.telegram.org/bot6863881576:AAFjOYMaXdH_K_OBUnuDGaKNfJFkOQfoMgc/sendMessage?chat_id=149273661&text='
				# url = url + urllib.parse.quote(name+" [HUNTER] "+ data)
				# threading.Thread(target=telegram, args=[url]).start()
			if start_hunter:
				start_bot()
			if follow_hunter and get_zone_name(get_position()['region']) not in ignoreZones and get_inventory()['items'][8]:
				mobs = get_monsters()
				stop_bot()
				stop_trace()
				follow_hunter = False
				QtBind.setChecked(gui2, cbxSro10, False)
				start_trace(data)
				Timer(5,stop_trace).start()
			if perma_trace and get_zone_name(get_position()['region']) not in ignoreZones and get_inventory()['items'][8]:
				inject_joymax(0x7150,b'\x01',True)
				Timer(1, inject_joymax,[0x7150, b'\x01', True]).start()
				Timer(2, inject_joymax,[0x7150, b'\x01', True]).start()
				Timer(3, inject_joymax,[0x7150, b'\x01', True]).start()
				Timer(4, inject_joymax,[0x7150, b'\x01', True]).start()
				Timer(5, inject_joymax,[0x7150, b'\x01', True]).start()
				Timer(6, inject_joymax,[0x7150, b'\x01', True]).start()
				Timer(7, inject_joymax,[0x7150, b'\x01', True]).start()
				perma_trace = False
				QtBind.setChecked(gui2, cbxSro11, perma_trace)
				stop_bot()
				start_trace(data)
			if pm_hunter and get_zone_name(get_position()['region']) not in ignoreZones and data not in pmList:
				pmList.append(data)
				phBotChat.Private('Seven', '['+data + '] -> ' + get_zone_name(get_position()['region']))
		elif t == 2 and data not in QtBind.getItems(gui2,lstOpcodes):
			log('[THIEF] '+data)
			if alertar_thief:
				play_wav('Sounds/Ladrones.wav')
			if dc_thief:
				Desconectar()
				Timer(1.0, os.kill, (os.getpid(), 9)).start()
			if party_thief:
				phBotChat.Party("THIEF: [" + data  + "]")
			if tlg_thief:
				name = get_character_data()['name']
				url = 'https://api.telegram.org/bot1221990015:AAHlL2X_NInc3xNo9MEnX_LHuSAEVa7VbqI/sendMessage?chat_id=149273661&text='
				url = url + urllib.parse.quote(name+" [THIEF] "+ data)
				threading.Thread(target=telegram, args=[url]).start()
			if start_thief:
				start_bot()
		if t == 2 and DC_trader:
			name = get_character_data()['name']
			if name != "Gari":
				Desconectar()
				while True:
					os.kill(os.getpid(), 9)

def startUnique():
	log('el bot iniciara en 1 segundo')
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['type'] == 24:
			set_training_position(0, mobs[mobID]['x'],mobs[mobID]['y'],0)
			start_bot()

def Dismount():
	pets = get_pets()
	for k, v in pets.items():
		if v['mounted']:
			inject_joymax(0x70CB, b'\x00'+struct.pack('I', k), False)
			return True
	return True

def DismountHorse():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
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
	pets = get_pets()
	if pets:
		for petID in pets:
			if pets[petID]['type'] == 'transport':
				return True
	return False

def useBanditScroll():
	for i,item in enumerate(get_inventory()['items']):
		if item and i > 12:
			if item['name'] == 'Bandit Den Return Scroll':
				inject_joymax(0x704C, struct.pack('b',i)+b'\xEC\x09', True)
				log('Bandit Den Return Scroll')
				return

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
	global energy
	global PICK
	if opcode == 0x7034: #put item equip wear
		if data[0] == 0:
			if '_THIEF_' in get_inventory()['items'][data[1]]['servername']:
				inject_joymax(0x7061, bytearray(), False)
				return Dismount()
	elif opcode == 0x3091:
		if data ==  b'\x00':
			joinParty(partyNumber)
			return False
		elif data ==  b'\x01':
			PICK = not PICK
			if PICK:
				notice('Pick activado')
			else:
				notice('Pick desactivado.')
			threading.Thread(target=pick_loop).start()
			return False
		elif data ==  b'\x02':
			followUnique()
			return False
	elif opcode == 0x706D:
		partyNumber = struct.unpack_from('<I', data, 0)[0]
		notice(str(partyNumber))
	elif opcode == 0x7402:
		energy = not energy
		if energy:
			notice('Energia Activada')
		else:
			notice('Energia Desactivada')
		useEnergy()
	return True

def followUnique():
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['type'] == 24:
			move_to(mobs[mobID]['x'],mobs[mobID]['y'],0)
			Timer(1,followUnique).start()
	return

def pick_loop():
	set_training_position(0,0,0,0)
	stop_trace()
	stop_bot()
	global PICK
	if PICK:
		drops = get_drops()
		pets = get_pets()
		if drops:
			for dropID in drops:
				if 'TRADE' in drops[dropID]['servername']:
					if pets:
						for slot, pet in pets.items():
							if pet['type'] == 'horse':
								inject_joymax(0x70CB, b'\x00'+struct.pack('I', slot), False) #dismount horse
							elif  pet['type'] == 'transport':
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
								for item in pet['items']:
									if item == None:
										Timer(0.5, pick_loop).start()
										return
								PICK = False
								useBanditScroll()
						spawnThiefPet()
						Timer(0.5, pick_loop).start()
						return
					else:
						spawnThiefPet()
						Timer(0.5, pick_loop).start()
						return
					break
		else:
			if pets:
				for slot, pet in pets.items():
					if pet['type'] == 'transport':
						PICK = False
						useBanditScroll()

def spawnThiefPet():
	inventory = get_inventory()
	items = inventory['items']
	for slot, item in enumerate(items):
		if item:
			if 'Goldclad Trade Horse' in item['name'] and len(get_drops()) < 10:
				log('Summoning: '+ item['name'])
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0xEC)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0xED)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				return
			elif len(get_drops()) > 9 and (item['name'] == 'Donkey' or 'elephant' in item['name'].lower()):
				log('Summoning: '+ item['name'])
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0xEC)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0xED)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				return
	for slot, item in enumerate(items):
		if item:
			if 'Goldclad Trade Horse' in item['name']:
				log('Summoning: '+ item['name'])
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0xEC)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0xED)
				Packet.append(0x11)
				inject_joymax(0x704C, Packet, True)
				return
	return False
					
def useEnergy():
	global energy
	if energy:
		for slot, item in enumerate(get_inventory()['items']):
			if item:
				if 'Energy of Life' in item['name']:
					Packet = bytearray()
					Packet.append(slot)
					Packet.append(0xEC)
					Packet.append(0x76)
					inject_joymax(0x704C, Packet, True)
					inject_joymax(0x715F, b'\x89\x5D\x00\x00\x81\x5D\x00\x00', True)
					Timer(0.5,useEnergy).start()
					return

def handle_chat(t,player,msg):
	global TelegramBol
	global partyNumber
	global comandos
	global attackWolf
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
		elif msg == '.a' and player == get_character_data()['name']:
			attackWolf = not attackWolf
			if attackWolf:
				morado('Wolf activado')
			else:
				morado('Wolf desactivado')
		elif msg == 'set' and get_character_data()['name'] == player:
			set_training_position(0, get_character_data()['x'], get_character_data()['y'], 0)

def useSpecialReturnScroll():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if x['name'] == 'Special Return Scroll' or x['name'] == 'Beginner Return Scroll':
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0xEC)
				Packet.append(0x09)
				inject_joymax(0x704C, Packet, True)
				break
		i+=1

def cancelReturnScroll():
	Packet = bytearray()
	inject_joymax(0x705B, Packet, False)
	log('Scroll cancelado')

def cancelscroll(s):
	useSpecialReturnScroll()
	Timer(0.5,cancelReturnScroll).start()
	return True

def verdemini(message):
	p = b'\x15\x06'+struct.pack('H', len(message))+message.encode('ascii') + b'\x00\xFF\x27\x00\x00'
	inject_silkroad(0x30CF,p,False)

def Union(message):
	message = ') '+message
	p = b'\x0B'
	p += struct.pack('H', len('Rahim'))
	p += 'Rahim'.encode('ascii')
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x3026,p,False)

def morado(message):
	p = struct.pack('B',7)
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x30CF,b'\x15'+p,False)

def rahim():
	global bolnotify
	if bolnotify:
		bolnotify = False
		azulPerma('Blue Notify By Rahim')

def handle_joymax(opcode, data):
	global UniqueTelegram
	global uniqueList
	global alarma
	global unionNotify
	if opcode == 0x3040 and len(data) == 23:
		verdemini(get_item(struct.unpack_from('i', data, 7)[0])['name']+' [Rahim]')
		return True
	elif opcode == 0xB069: #Party Form
		partyNumber = struct.unpack_from('I', data, 1)[0]
		notice(str(partyNumber))
	elif opcode == 0x304E and data[0] == 4:
		if struct.unpack_from('b', data, 1)[0] == 5 and ScrollAfterZerk:
			useSpecialReturnScroll()
			stop_bot()
			morado('Zerk By Rahim.')
	elif opcode == 0x3864 and data:
		if struct.unpack_from('<s', data, 0)[0] == b'\x02':
			name = struct.unpack_from('<' + str(data[6]) + 's',data,8)[0].decode('cp1252')
			mobs = get_monsters()
			for mobID in mobs:
				if mobs[mobID]['type'] == 24:
					phBotChat.Party(name + ' Here! => ['+mobs[mobID]['name'] +']')
					break
	elif opcode == 0xB034 and len(data)>7:
		dropType = struct.unpack_from('h', data, 0)[0]
		if dropType == 4353 or dropType == 7169:
			itemID = get_item(struct.unpack_from('I', data, 11)[0])
			itemName = itemID['name']
			if 'Poro' in itemID['name']:
				itemName = 'Poro Balloon'
			for item in itemListAzul:
				if item in itemName.lower():
					azulPerma('['+itemName +'] gained.')
					break
			if itemID['rare']:
				azulPerma('['+itemName +'] gained.')
			if unionNotify:
				for item in otrosItems:
					if item == itemName:
						Union('['+itemName+'] gained')
		if dropType == 1537:#1537
			itemID = get_item(struct.unpack_from('I', data, 7)[0])
			itemName = itemID['name']
			if 'Poro' in itemID['name']:
				itemName = 'Poro Balloon'
			for item in itemListAzul:
				if item in itemName.lower():
					azulPerma('['+itemName +'] gained.')
					break
			if itemID['rare']:
				azulPerma('['+itemName +'] gained.')
			if unionNotify:
				log('union yes')
				for item in otrosItems:
					if item == itemName:
						Union('['+itemName+'] gained')
		if dropType == 1537 or dropType == 4353 or dropType == 7169:
			Timer(10,rahim).start()
	elif opcode == 0x3068: #party item droped distributed
		itemName = get_item(struct.unpack_from('<I', data, 4)[0])['name']
		playerName = get_party()[struct.unpack_from('<I', data, 0)[0]]['name']
		if 'Poro' in itemName:
			itemName = 'Poro Balloon'
		for item in itemListAzul:
			if item in itemName.lower():
				azulPerma('['+itemName +']is distributed to ['+ playerName+']')
				# phBotChat.Party('item ['+itemName +']is distributed to ['+ playerName+']')
				break
		if get_item(struct.unpack_from('<I', data, 4)[0])['rare']:
			azulPerma('['+itemName +']is distributed to ['+ playerName+']')
		if unionNotify:
			for item in otrosItems:
				if item == itemName:
					Union('['+itemName +']is distributed to ['+ playerName+']')
		Timer(12,rahim).start()
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
	elif opcode == 0x30CF: #Mensajes de eventos
		if data == b'\x15\x02\x55\x00\x59\x6F\x75\x20\x6D\x75\x73\x74\x20\x63\x6F\x6D\x70\x6C\x65\x74\x65\x20\x74\x68\x65\x20\x63\x61\x70\x74\x63\x68\x61\x20\x76\x65\x72\x69\x66\x63\x61\x74\x69\x6F\x6E\x20\x74\x6F\x20\x70\x72\x6F\x63\x65\x65\x64\x20\x77\x69\x74\x68\x20\x62\x75\x79\x69\x6E\x67\x2F\x73\x65\x6C\x6C\x69\x6E\x67\x20\x74\x72\x61\x64\x65\x20\x67\x6F\x6F\x64\x73\x2E': # Trader Sell
			deleteClean()
	elif opcode == 0xB070 and attackWolf: #MOB_ATTACKED
		pets = get_pets()
		if pets:
			for pet, v in pets.items():
				if v['type'] == 'wolf':
					victima = struct.unpack_from('I', data, 15)[0]
					if victima == get_character_data()['player_id'] or victima == pet:
						mob = struct.unpack_from('I', data, 7)[0]
						if mob not in mobAtacked:
							mobAtacked.append(mob)
						tempMob = 0
						for mob in mobAtacked:
							if mob in get_monsters():
								morado(str(mob))
								if mob > tempMob:
									tempMob = mob
							else:
								mobAtacked.remove(mob)
								break
						inject_joymax(0x70C5, struct.pack('i', pet) + b'\x02' + struct.pack('i', tempMob), False)
	return True

def sendTelegram(data):
	global idTelegram
	url = 'https://api.telegram.org/bot6863881576:AAFjOYMaXdH_K_OBUnuDGaKNfJFkOQfoMgc/sendMessage?chat_id='+idTelegram+'&parse_mode=Markdown&text='
	if '_' in data:
		url = 'https://api.telegram.org/bot6863881576:AAFjOYMaXdH_K_OBUnuDGaKNfJFkOQfoMgc/sendMessage?chat_id='+idTelegram+'&text='
	url = url + urllib.parse.quote(data)
	urllib.request.urlopen(url,context=ssl._create_unverified_context())
	saveConfig()

def notice(message):
	p = struct.pack('B',7)
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x3026,p,False)

def azulPerma(message):
	p = b'\x15\x04'
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x30CF,p,False)

def joined_game():
	morado('SuperPlugin Version 4.5 By Rahim')

def checkThief(time):
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['name'] == 'Thief':
			notice('Thief NPC')
			return
	if time < 3:
		Timer(time,checkThief,[time+1]).start()

def moveToBandit():
	x1 = 9113
	y1 = 876
	x2 = get_position()['x']
	y2 = get_position()['y']
	dis = ((x2-x1)**2+(y2-y1)**2)**1/2
	if dis > 30:	
		move_to(x1,y1,0)
		Timer(0.5,moveToBandit).start()
		return

def teleported():
	global ScrollAfterZerk
	global energy
	global gui
	global attackWolf
	global bolnotify
	global count
	bolnotify = False
	attackWolf = False
	ScrollAfterZerk = False
	QtBind.setChecked(gui, scrollCheck, ScrollAfterZerk)
	energy = False
	pmList = []
	quests = get_quests()
	if count:
		Timer(2,inject_joymax,[0xA451,b'\x04',True]).start()
	for questID in quests:
		if quests[questID]['completed']:
			notice('Pendint Quest! By Rahim')
			break
	if get_zone_name(get_character_data()['region']) == 'Diebesstadt':
		stop_bot()
		moveToBandit()

def deleteClean():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['type'] == 'transport':
				for item in v['items']:
					if item != None:
						Timer(0.5,deleteClean).start()
						return
				break
	else:
		exitBandit()
	if v['type'] == 'pick' or v['type'] == 'wolf':
		exitBandit()
		return
	if get_zone_name(get_character_data()['region']) == 'Diebesstadt':
		inject_joymax(0x70C6, struct.pack('I', k), False)
	Timer(1,deleteClean).start()

def exitBandit():
	for i,x in enumerate(get_inventory()['items']):
		if x and i > 12:
			if x['name'] == 'Bandit Den Return Scroll':
				if x['quantity'] <= 10:
					notice('BANDIT SCROLLS!')
					return

for unique in uniqueList:
	QtBind.append(gui,qtUniqueList,unique)

log("[Super Plugin v4.7 by Rahim]")
