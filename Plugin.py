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
dropTelegram = False
white_list = ['Ross','Asterith','27CM','KLR','Space','SpaceJis','Grego','Suarez','Hamtay','AIICaps','Auron','AllCaps','Dalton','Hamtay','Kalimyst','KaIimyst','Hamtay','THE_BARD','THE_BARD1','THE_CHINITO','TH3_WIZARD','THE_WIZARD','THE_CLERIK','THE_MAST3R','THE_WARRIOR','_AkaZa','_Kirby_','NoSoyBardo','xShuTheFckUp','_BlooD_','xAeon','xTremeCreW_','_Yazsoke_']
VIP = False

if get_character_data()['name'] in white_list:
	VIP = True

start = False
n = 10
R = 35
lideres = ['Seven','Zoser','Norte','dCarnage']
filename = 'Script.txt'
goUnique = True
murio_tierra = False
display = 0
mob_killed = 0
JUPITER_ID = False
YUNO_SPAWNED = bytes.fromhex('1C 0C 02 1D 00 55 49 49 54 5F 53 54 54 5F 57 4F 52 53 48 49 50 5F 59 55 4E 4F 5F 53 50 41 57 4E 45 44')
JUPITER_SPAWNED = bytes.fromhex('1C 0C 02 20 00 55 49 49 54 5F 53 54 54 5F 57 4F 52 53 48 49 50 5F 4A 55 50 49 54 45 52 5F 53 50 41 57 4E 45 44')
token2 = urlopen('https://raw.githubusercontent.com/RahimSRO/Serapis/refs/heads/main/test.txt').read().decode("utf-8")[:-1]
token = urlopen('https://raw.githubusercontent.com/RahimSRO/Serapis/refs/heads/main/test2.txt').read().decode("utf-8")[:-1]

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
	global dropTelegram
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
			if 'dropTelegram' in json_object:
				dropTelegram = json_object['dropTelegram']
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
	global dropTelegram
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
		'dropTelegram': dropTelegram
	}

	# Serializing json
	json_object = json.dumps(dictionary, indent=4)
	 
	# Writing to sample.json
	with open("sample.json", "w") as outfile:
	    outfile.write(json_object)

mobAtacked = []
attackWolf = False
itemListAzul = ['advanced','sharpness','lottery','silk scroll','immortal','lucky','poro','sabakun','coin','blue stone','serapis', 'black stone']
otrosItems = ['Reverse Reverse Return Scroll','Global chatting','Magic POP Card']
PICK = False
energy = False
pmList = []
WhiteList = ['Seven','Cbum','Kurumi','Moshi','Zoser','Fami', 'Pomi', 'Lestrange','OnlyClerid','Dooster']
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

if get_character_data()['name'] in WhiteList and False:
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
dropTelegramCheck = QtBind.createCheckBox(gui,'checkDrop','Drop Telegram',10,250)

lstOpcodes = QtBind.createList(gui,621,30,100,80)
btnRemOpcode = QtBind.createButton(gui,'removeIgnore',"     GO & BOT     ",635,113)
btnAddOpcode = QtBind.createButton(gui,'llenarLista',"      REFRESH      ",630,10)

lblOpcodes = QtBind.createLabel(gui,"Unique List",321,110)
qtUniqueAdd = QtBind.createLineEdit(gui,"",321,129,100,20)
qtUniqueList = QtBind.createList(gui,321,151,176,109)
btnAddOpcode = QtBind.createButton(gui,'addUnique',"      Add      ",423,129)
btnRemOpcode = QtBind.createButton(gui,'removeUnique',"     Remove     ",370,259)

def sendTelegram2(data='quest'):
	global token2
	if data[0] == 'sendTelegram':
		data = 'quest'
	url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id=149273661&parse_mode=Markdown&text='
	url = url + urllib.parse.quote(data)
	urllib.request.urlopen(url,context=ssl._create_unverified_context())
	return True

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
QtBind.setChecked(gui, dropTelegramCheck, dropTelegram)

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

def checkDrop(checked):
	global dropTelegram
	dropTelegram = checked
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
					set_training_script('')
					set_training_position(Party[memberID]['region'], Party[memberID]['x'], Party[memberID]['y'], 0.0)
					start_bot()

def handle_event(t, data):
	global VIP
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
	global dropTelegram
	if VIP:
		if t == 0:
			bolnotify = True
			notice(data)
			if partyAlert and 'Ballon' not in data:
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
		if get_character_data()['name'] in WhiteList and False:
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
		elif t == 5:
			log('xd')
			if dropTelegram:
				threading.Thread(target=sendTelegram, args=['*'+get_character_data()['name'] + '* -> `'+get_item(int(data))['name']+'`'],).start()

def startUnique():
	log('el bot iniciara en 1 segundo')
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['type'] == 24:
			set_training_position(0, mobs[mobID]['x'],mobs[mobID]['y'],0)
			start_bot()

def Dismount():
	pets = get_pets()
	if pets:
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

def is_master():
	Party = get_party()
	if Party:
		for memberID in Party:
			if get_character_data()['name'] == Party[memberID]['name']:
				return memberID
			else:
				return False
	return False

def handle_silkroad(opcode,data):
	global VIP
	global partyNumber
	global energy
	global PICK
	if VIP:
		if opcode == 0x7034: #put item equip wear
			if data[0] == 0:
				if '_THIEF' in get_inventory()['items'][data[1]]['servername']:
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
	global VIP
	global TelegramBol
	global partyNumber
	global comandos
	global attackWolf
	global start
	global actual
	global tiempo
	global lideres
	global goUnique
	global filename
	global murio_tierra
	global mob_killed
	global goUnique
	global R
	global JUPITER_ID
	if VIP:
		if t == 2:
			if TelegramBol:
				threading.Thread(target=sendTelegram, args=[player + " -> " + get_character_data()['name'] + ' -> ' + msg],).start()
			foo = msg.split()
			for word in foo:
				if word.isnumeric():
					notice(word)
					partyNumber = int(word)
					break
		elif msg[0] == '~' and t == 4 and msg[1:].isnumeric():
			Party = get_party()
			if Party:
				for memberID in Party:
					if memberID == int(msg[1:]):
						Dismount()
						log('Dismounted')
					else:
						return
		elif msg == 'spawn':
			JUPITER_ID = False
			goUnique = True
			mob_killed = 0
			filename = 'Script.txt'
			murio_tierra = False
			if is_master():
				spawn_dimension()
		elif get_character_data()['name'] == player and msg == 'comandos':
			notice("tptg")
			notice("tpcerb")
			notice("tpuru1")
			notice("tpuru2")
			notice("tpivy1")
			notice("tpisy1")
			notice("tpisy2")
			notice("tpisy3")
			notice("tplord1")
			notice("tplord2")
			notice("tproc1")
			notice("tproc2")
			notice("tpred")
			notice("tpforest")
			notice("tpb4")
		if msg == 'stop':
			partyNumber == 0
		if comandos:
			if msg == 'stop':
				stop_trace()
				stop_bot()
			elif msg == 'scroll':
				useSpecialReturnScroll()
			elif msg == 'follow':
				stop_bot()
				stop_trace()
				if get_character_data()['name'] != player:
					start_trace(player)
			elif msg == 'start':
				stop_trace()
				start_bot()
			elif get_character_data()['name'] == player and msg[0:2] == '>>' and msg[3] != ' ':
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
			elif t == 4 and ',' in msg and msg.replace(',','').replace('-','').isnumeric():
				log('Coordenadas')
				stop_trace()
				stop_bot()
				set_training_script('')
				region = msg.split(',')[0]
				x = msg.split(',')[1]
				y = msg.split(',')[2]
				set_training_position(int(region), int(x), int(y), 0)
				if get_training_area()['radius'] == 0:
					set_training_radius(20)
				start_bot()
			elif get_character_data()['name'] == player and msg[:2] == ':>':
				log('Cambiando a perfil -> '+msg[2:])
				set_profile(msg[2:])
			elif player == get_character_data()['name'] and msg == 'tomb':
				stop_trace()
				stop_bot()
				reverse_return(3, "Seenwald")
			elif player == get_character_data()['name'] and msg == 'tptg':
				stop_trace()
				stop_bot()
				reverse_return(3, "Bandit-Bergfestung")
			elif player == get_character_data()['name'] and msg == 'tpdemon':
				stop_trace()
				stop_bot()
				reverse_return(3, "Heart Peak")
			elif player == get_character_data()['name'] and msg == 'tpuru1':
				stop_trace()
				stop_bot()
				reverse_return(3, "Black-Robber-Lager")
			elif player == get_character_data()['name'] and msg == 'tpuru2':
				stop_trace()
				stop_bot()
				reverse_return(3, "Tarimbecken")
			elif player == get_character_data()['name'] and msg == 'tplord1':
				stop_trace()
				stop_bot()
				reverse_return(3, "Niya-Ruine")
			elif player == get_character_data()['name'] and msg == 'tplord2':
				stop_trace()
				stop_bot()
				reverse_return(3, "Fruchtbarkeitstempel")
			elif player == get_character_data()['name'] and msg == 'tpisy1':
				stop_trace()
				stop_bot()
				for i,x in enumerate(get_inventory()['items']):
					if x and i > 13:
						if x['name'] == 'Reverse Reverse Return Scroll':
							inject_joymax(0x704C, struct.pack('b',i)+b'\xED\x19\x07\x14\x00\x00\x00', False)
							return
			elif player == get_character_data()['name'] and msg == 'tpisy2':
				stop_trace()
				stop_bot()
				for i,x in enumerate(get_inventory()['items']):
					if x and i > 13:
						if x['name'] == 'Reverse Reverse Return Scroll':
							inject_joymax(0x704C, struct.pack('b',i)+b'\xED\x19\x07\x15\x00\x00\x00', False)
							return
			elif player == get_character_data()['name'] and msg == 'tpisy3':
				stop_trace()
				stop_bot()
				for i,x in enumerate(get_inventory()['items']):
					if x and i > 13:
						if x['name'] == 'Reverse Reverse Return Scroll':
							inject_joymax(0x704C, struct.pack('b',i)+b'\xED\x19\x07\x13\x00\x00\x00', False)
							return
			elif player == get_character_data()['name'] and msg == 'tproc':
				stop_trace()
				stop_bot()
				reverse_return(3, "Herzgipfel")
			elif player == get_character_data()['name'] and msg == 'tproc2':
				stop_trace()
				stop_bot()
				reverse_return(3, "Windstadt")
			elif player == get_character_data()['name'] and msg == 'tpivy':
				stop_trace()
				stop_bot()
				reverse_return(3, "Cleopatra-Tor")
			elif player == get_character_data()['name'] and msg == 'tpivy2':#no funciona
				stop_trace()
				stop_bot()
				reverse_return(3, "Teich-Ruinen")
			elif player == get_character_data()['name'] and msg == 'tphwt':#no funciona
				stop_trace()
				stop_bot()
				reverse_return(3, "Roter Boden")
			elif player == get_character_data()['name'] and msg == 'tpcerb':
				stop_trace()
				stop_bot()
				reverse_return(3, "Göttergarten")
			elif player == get_character_data()['name'] and msg == 'tpred':
				stop_trace()
				stop_bot()
				for i,x in enumerate(get_inventory()['items']):
					if x and i > 13:
						if x['name'] == 'Reverse Reverse Return Scroll':
							inject_joymax(0x704C, struct.pack('b',i)+b'\xED\x19\x07\x29\x00\x00\x00', False)
							return
			elif player == get_character_data()['name'] and msg == 'tpforest':
				stop_trace()
				stop_bot()
				reverse_return(3, "Kummerwald")
			elif player == get_character_data()['name'] and msg == 'tpb4':
				stop_trace()
				stop_bot()
				for i,x in enumerate(get_inventory()['items']):
					if x and i > 13:
						if x['name'] == 'Reverse Reverse Return Scroll':
							inject_joymax(0x704C, struct.pack('b',i)+b'\xED\x19\x07\x26\x00\x00\x00', False)
							return
			elif msg == 'r/' and get_character_data()['name'] != player:
				for slot, item in enumerate(get_inventory()['items']):
					if slot > 13 and item:
						if item['name'] == 'Special Reverse Return':
							data = struct.pack('H', len(player)) + player.encode('ascii') + struct.pack('b', slot)
							log((' '.join('{:02X}'.format(x) for x in data)))
							inject_joymax(0xA459,data,True)
							return True
			elif msg == 'tlp':
				tlp()


def useSpecialReturnScroll():
	for i,x in enumerate(get_inventory()['items']):
		if x and i > 13:
			if x['name'] == 'Special Return Scroll':
				log('Usando: '+x['name'])
				inject_joymax(0x704C, struct.pack('B',i)+b'\xEC\x09',True)
				return
	log('No hay retun scrol...')

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

def purple(message):
	p = b'\x15\x06'+struct.pack('H', len(message))+message.encode('ascii') + b'\xEE\x88\xA7\x00\x01'
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
	global VIP
	global UniqueTelegram
	global uniqueList
	global alarma
	global unionNotify
	global dropTelegram
	global tiempo
	global lideres
	global filename
	global mob_killed
	global actual
	global JUPITER_ID
	if VIP:
		if opcode == 0x3056 and get_zone_name(get_character_data()['region']) == 'Anbetungshalle':
			tiempo[1] = time.time()
			mob_killed +=1
			log(f'Mobs: {mob_killed}')
			if struct.unpack_from('I',data,0)[0] == JUPITER_ID and get_character_data()['name'] in lideres:
				red(f'Murio Jupiter')
				log(f'Murio Jupiter')
				Timer(5,exitFGW).start()
				log((' '.join('{:02X}'.format(x) for x in data)))
				return True
		elif opcode == 0x751A:
			inject_joymax(0x751C,data[:4]+b'\x00\x00\x00\x00\x01',False) #accept FGW request
			log('Acepting FGW request.')
			red('Acepting FGW request.')
		if opcode == 0x3040 and len(data) == 23:
			verdemini(get_item(struct.unpack_from('i', data, 7)[0])['name']+' [Rahim]')
			return True
		elif opcode == 0xB069 and data != b'\x02\x20\x2C': #Party Form
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
					if mobs[mobID]['type'] == 24 and 'Ballon' not in mobs[mobID]['name']:
						phBotChat.Party(name + ' Here! => ['+mobs[mobID]['name'] +']')
						break
		elif opcode == 0xB034 and len(data)>3:
			dropType = struct.unpack_from('h', data, 0)[0]
			if dropType == 4353 or dropType == 7169:
				itemID = get_item(struct.unpack_from('I', data, 11)[0])
				itemName = itemID['name']
				if struct.unpack_from('I', data, 11)[0] > 33892 and struct.unpack_from('I', data, 11)[0] < 33901:
					azulPerma(f'item [{itemName}] gained.')
					playerName = get_character_data()['name']
					sendTelegram2(f'`{itemName}` Gained. ---> `{playerName}`')
				if 'Poro' in itemID['name']:
					itemName = 'Poro Balloon'
				for item in itemListAzul:
					if item in itemName.lower():
						azulPerma('['+itemName +'] gained.')
						break
				if itemID['rare']:
					msg = '['+itemName +'] gained.'
					azulPerma(msg)
					if dropTelegram:
						sendTelegram(msg)
				if unionNotify:
					for item in otrosItems:
						if item == itemName:
							Union('['+itemName+'] gained')
			if dropType == 1537:
				itemID = get_item(struct.unpack_from('I', data, 7)[0])
				itemName = itemID['name']
				if struct.unpack_from('I', data, 7)[0] > 33892 and struct.unpack_from('I', data, 7)[0] < 33901:
					azulPerma(f'item [{itemName}] gained.')
					playerName = get_character_data()['name']
					sendTelegram2(f'`{itemName}` Gained. ---> `{playerName}`')
				if 'Poro' in itemID['name']:
					itemName = 'Poro Balloon'
				for item in itemListAzul:
					if item in itemName.lower():
						azulPerma('['+itemName +'] gained.')
						break
				if itemID['rare']:
					msg = '['+itemName +'] gained.'
					azulPerma(msg)
					if dropTelegram:
						sendTelegram(msg)
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
			if struct.unpack_from('<I', data, 4)[0] > 33892 and struct.unpack_from('<I', data, 4)[0] < 33901:
				msg = f'item [{itemName}] is distributed to [{playerName}]'
				azulPerma(msg)
				sendTelegram2(f'item `{itemName}` is distributed to `{playerName}`')
			if 'Poro' in itemName:
				itemName = 'Poro Balloon'
			for item in itemListAzul:
				if item in itemName.lower():
					azulPerma('['+itemName +']is distributed to ['+ playerName+']')
					# phBotChat.Party('item ['+itemName +']is distributed to ['+ playerName+']')
					break
			if get_item(struct.unpack_from('<I', data, 4)[0])['rare']:
				msg = '['+itemName +']is distributed to ['+ playerName+']'
				azulPerma(msg)
				if dropTelegram:
					sendTelegram(msg)
			if unionNotify:
				for item in otrosItems:
					if item == itemName:
						Union('['+itemName +']is distributed to ['+ playerName+']')
			Timer(12,rahim).start()
		elif opcode == 0x300C and data[0] == 5: # Unique Spawn
			if data == YUNO_SPAWNED:
				azulPerma('Yuno spawned')
				earth()
			if data == JUPITER_SPAWNED:
				azulPerma('Jupiter spawned')
				if get_character_data()['name'] in lideres:
					filename = 'Jupiter.txt'
					phBotChat.Party('stop')
					phBotChat.Party('true')
					phBotChat.Party('zerc')
					start_no_drop()
				elif 'UIIT_STT_JUPITER_A_' in str(data):
					azulPerma(f'Puerta: {str(data)[-4:-1]}')
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
		elif opcode == 0xB070:
			if len(data) > 3:
				mobs = get_monsters()
				for mobID in mobs:
					if mobs[mobID]['type'] == 24:
						if struct.unpack_from('I', data, 3)[0] == 12294:
							azulPerma("Petrificado xD")
			if attackWolf: #MOB_ATTACKED
				pets = get_pets()
				if pets:
					for pet, v in pets.items():
						if v['type'] == 'wolf':
							victima = struct.unpack_from('<I', data, 15)[0]
							if victima == get_character_data()['player_id'] or victima == pet:
								mob = struct.unpack_from('<I', data, 7)[0]
								if mob not in mobAtacked and get_monsters()[mob]['type'] != 24:
									mobAtacked.append(mob)
								tempMob = 0
								for mob in mobAtacked:
									mobs = get_monsters()
									for mobID in mobs:
										if mobID == mob and mob > tempMob:
											tempMob = mob
											break
									mobAtacked.remove(mob)
								inject_joymax(0x70C5, struct.pack('i', pet) + b'\x02' + struct.pack('i', tempMob), False)
								log('Atacando a :' +str(tempMob))
								log(str(mobAtacked))
								return True
				return True
	return True

def exitFGW():
	log('exitFGW')
	if get_drops():
		Timer(1,exitFGW).start()
	else:
		phBotChat.All('scroll')
		phBotChat.All('stop')
		# phBotChat.All(':>1')
		# Timer(1,phBotChat.Party['f']).start()

def sendTelegram(data):
	global idTelegram
	global token
	url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={idTelegram}&parse_mode=Markdown&text='
	if '_' in data:
		url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={idTelegram}&text='
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
	global white_list
	global VIP
	if get_character_data()['name'] in white_list:
		VIP = True
	else:
		purple('El plugin es privado, para FGW y Uniques. Contactar a su creador para mas info...')


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
	global murio_tierra
	global filename
	global lideres
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
	elif get_zone_name(get_character_data()['region']) == 'The Earths Raum':
		delete_pet()
	elif get_zone_name(get_character_data()['region']) == 'Anbetungshalle':
		Timer(4,delete_pet).start()
		stop_trace()
		if is_master():
			log('Soy master')
			phBotChat.Party('~'+str(is_master()))
			Timer(1,move_to_npc,[19480,6425]).start()
			threading.Thread(target=sendTelegram2, args=['Dimension   `'+get_character_data()['name']+'`']).start()
		else:
			go_to_buff(32236,19480,6425,839)
			if get_character_data()['name'] in lideres and murio_tierra:
				filename = 'Yuno.txt'
			if get_character_data()['name'] in lideres:
				log('dire k en all en 20 seg')
				Timer(20,phBotChat.All,['k']).start()

def go_to_buff(region,x,y,z):
	log('go_to_buff')
	x1 = get_position()['x']
	y1 = get_position()['y']
	dis = ((x-x1)**2+(y-y1)**2)**1/2
	move_to(x,y,0)
	if dis < 5:
		set_training_position(region, x, y, z)
		Timer(1,start_bot).start()
		return
	Timer(0.2,go_to_buff,[region, x, y, z]).start()
	# log(str(dis))

def call_one_for_one(slot,id):
	log('call_one_for_one')
	if slot < 8:
		Party = get_party()
		for i,memberID in enumerate(Party):
			if i == slot:
				log(f'calling: ' {get_party()[memberID]['name']})
				red(f'calling: ' {get_party()[memberID]['name']})
				inject_joymax(0x751A, struct.pack('I',memberID), False)
				Timer(0.5,call_one_for_one,[slot+1,id]).start()
				return
	log('Exit NPC')
	red('Exit NPC')
	inject_joymax(0x704B, struct.pack('L', id), False)
	set_training_position(0, 19480, 6425, 0)
	start_bot()

def spawn_dimension():
	for slot, item in enumerate(get_inventory()['items']):
		if slot > 13 and item:
			if 'Hall of Worship (Level 1)' in item['name']:
				inject_joymax(0x704C, struct.pack('b', slot)+b'\x6C\x3E', True)
				log('Spawming dimension...')
				return

def talk_npc():
	npcs = get_npcs()
	for id, npc in npcs.items():
		if npc['name'] == 'Säule zum Rückruf der Gruppenmitglieder':
			inject_joymax(0x7045, struct.pack('L', id), False)
			log('Selecting NPC')
			Timer(1,inject_joymax,[0x7519, struct.pack('L', id), False]).start()
			Timer(1.5,log,['Starting to call members...']).start()
			Timer(2,call_one_for_one,[0,id]).start()
			return

def move_to_npc(x,y):
	phBotChat.Party('~'+str(is_master()))
	log('move_to_npc')
	x1 = get_position()['x']
	y1 = get_position()['y']
	dis = ((x-x1)**2+(y-y1)**2)**1/2
	move_to(x,y,0)
	if dis > 5:
		talk_npc()
		return
	Timer(0.2,move_to_npc,[x,y]).start()

def delete_pet():
	log('delete_pet')
	pets = get_pets()
	if pets:
		for petID in pets:
			if pets[petID]['type'] == 'wolf':
				inject_joymax(0x7116, struct.pack('i',petID) + b'\x00', True)
				Timer(0.5,delete_pet).start()
				return

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

def start_no_drop():
	if not get_drops():
		phBotChat.All('k')
		return
	Timer(1,start_no_drop).start()

def earth():
	log('earth')
	global murio_tierra
	global start
	if get_zone_name(get_character_data()['region']) == 'The Earths Raum':
		if not get_monsters():
			start = False
			x1 = get_position()['x']
			y1 = get_position()['y']
			x = -20832
			y = 101
			move_to(x,y,-134)
			dis = ((x-x1)**2+(y-y1)**2)**1/2
			if dis < 2 and not get_drops() and get_npcs():
				murio_tierra = True
				tlp()
				return
		Timer(1,earth).start()

def tlp():
	inject_joymax(0x705B, bytearray(), False)
	npcs = get_npcs()
	for id, npc in npcs.items():
		# log(npc['name'])
		if npc['name'] == 'Tunnelaufseher Salhap':#Tunel 1
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x1E\x00\x00\x00', False)
		elif npc['name'] == 'Tunnelaufseher Maryokuk':
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x1B\x00\x00\x00', False)
		elif npc['name'] == 'Tunnelaufseher Topni': #Tunel 2
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x1D\x00\x00\x00', False)
		elif npc['name'] == 'Tunnelaufseher Asui':
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x1A\x00\x00\x00', False)
		elif npc['name'] == 'Ferry Ticket Seller Hageuk': #Jangan West
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x09\x00\x00\x00', False)
		elif npc['name'] == 'Ferry Ticket Seller Chau':
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x06\x00\x00\x00', False)
		elif npc['name'] == 'Ferry Ticket Seller Doji': #Jangan East
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x04\x00\x00\x00', False)
		elif npc['name'] == 'Ferry Ticket Seller Tayun':
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x03\x00\x00\x00', False)
		elif npc['name'] == 'Boat Ticket Seller Rahan': #Hotan Ravine
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x0E\x00\x00\x00', False)
		elif npc['name'] == 'Boat Ticket Seller Salmai':
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x0C\x00\x00\x00', False)
		elif npc['name'] == 'Boat Ticket Seller Asa': #Hotan Black Robber
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x0D\x00\x00\x00', False)
		elif npc['name'] == 'Boat Ticket Seller Asimo':
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x0F\x00\x00\x00', False)
		elif npc['name'] == 'Flugkartenverkäuferin Shard': #Ivy
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x1F\x00\x00\x00', False)
		elif npc['name'] == 'Flugkartenverkäuferin Sangnia':
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x18\x00\x00\x00', False)
		elif npc['name'] == 'Harbor Manager Marwa' or npc['name'] == 'Pirate Morgun': #Alexandria
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x15\x00\x00\x00', False)
		elif npc['name'] == 'Harbor Manager Gale': #Dock
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x16\x00\x00\x00', False)
		elif npc['name'] == 'Pirate Blackbeard': #Sigia
			inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x15\x00\x00\x00', False)
		elif npc['name'] == 'Grab des Kaisers Qin-Shi Lv.4': #Medusa
			inject_joymax(0x705A, struct.pack('h',id)+b'\x00\x00\x03\x00', False)
		elif npc['name'] == 'Dimensionslücke':
			log('Teleporting to dimension area.')
			red('Teleporting to dimension area.')
			Dismount()
			inject_joymax(0x705A, struct.pack('I',id)+b'\x03\x00', False)



version = '4.0.0'
ver = QtBind.createLabel(gui,'v'+version,690,300)
log('[Super Plugin v'+version+' by Rahim]')
