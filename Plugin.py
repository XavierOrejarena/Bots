
# log((' '.join('{:02X}'.format(x) for x in data)))
from phBot import *
import struct
import QtBind
import threading
from threading import Timer
import phBotChat
import os
from time import sleep
import urllib.request
import random
import signal
import ssl
import subprocess
import sys
from math import pi, cos, sin
from random import random

def point(x1,y1):
	r = 2
	global partyNumber
	if partyNumber != 0:
		theta = random() * 2 * pi
		move_to(int(x1 + cos(theta) * r),int(y1 + sin(theta) * r),0)
		Timer(0.2,point,[x1,y1]).start()

myPlayers = ['Seven','Zoser','Trump','Cuantica','Amor','Paz','Yeico','Sol','Amanda','Rah','How']

def cancelAlchemy():
	inject_joymax(0x7150,b'\x01',True)
	Timer(1, inject_joymax,[0x7150, b'\x01', True]).start()
	Timer(2, inject_joymax,[0x7150, b'\x01', True]).start()
	Timer(3, inject_joymax,[0x7150, b'\x01', True]).start()
	Timer(4, inject_joymax,[0x7150, b'\x01', True]).start()
	Timer(5, inject_joymax,[0x7150, b'\x01', True]).start()
	Timer(6, inject_joymax,[0x7150, b'\x01', True]).start()
	Timer(7, inject_joymax,[0x7150, b'\x01', True]).start()
	quitarDressLucky()

def disconnected():
	# urllib.request.urlopen('https://api.telegram.org/bot1221990015:AAHlL2X_NInc3xNo9MEnX_LHuSAEVa7VbqI/sendMessage?chat_id=149273661&text=DC',context=ssl._create_unverified_context())
	log('HAS SIDO DESCONECTADO TIO')
	global TelegramBol
	# if TelegramBol:
	# 	os.kill(os.getpid(), 9)

energy = False
thiefs = ['_4Fun','Aleen','MrSaba','Yako','Sub_ZerO','NukerSouL','CarTeR3','Newfasta','_HolaWorld_','SwordOfChaoS','MickeyMousE','JaackNC']
merca = False
partyAlert = True
USTR = False
UINT = False
dropg = False
gui = QtBind.init(__name__,'Miscelaneos')
ignore = ['[BOT]System','[BOT]Evento','[BOT]Evento1','[BOT]Evento2','Seven','Zoser']
uniques = ["Tiger Girl","Cerberus","Captain Ivy","Uruchi","Isyutaru","Lord Yarkan","Demon Shaitan","White Knight","Homocidal Santa"]
NotificarCheck = QtBind.createCheckBox(gui,'Notificar','Notificar Chat',70,10)
partyAlertCheck = QtBind.createCheckBox(gui,'partyAlertChecker','Party Alert',90,40)
QtBind.setChecked(gui, NotificarCheck, True)
QtBind.setChecked(gui, partyAlertCheck, partyAlert)
TelegramBol = True
zones = ['Lost Lake','Samarkand','Jangan']
ignoreZones = ['Samarkand','Jangan','Königreich Hotan','Western-China-Donwhang','Constantinople']
jelp = False
partyNumber = 0
NPC = False
drop = True
dropItems		= QtBind.createButton(gui,'exitBandit','exitBandit',250,220)
partyList = QtBind.createList(gui,120,180,100,80)
btnRemove = QtBind.createButton(gui,'remove',"     GO & BOT     ",130,259)
btnFill = QtBind.createButton(gui,'llenarLista',"      REFRESH      ",130,160)

def llenarLista():
	QtBind.clear(gui,partyList)
	Party = get_party()
	if Party:
		for memberID in Party:
			if Party[memberID]['name'] != get_character_data()['name']:
				QtBind.append(gui,partyList,Party[memberID]['name'])

def remove():
	selectedItem = QtBind.text(gui,partyList)
	if selectedItem:
		Party = get_party()
		if Party:
			for memberID in Party:
				if selectedItem == Party[memberID]['name']:
					set_training_position(Party[memberID]['region'], Party[memberID]['x'], Party[memberID]['y'], 0.0)
					start_bot()


def talkToBandit():
	npcs = get_npcs()
	for id, npc in npcs.items():
		if "gestohlener Waren" in npc['name']:
			inject_joymax(0x7045, struct.pack('I',id), False)
			Timer(0.5, inject_silkroad,[0xB034, b'\x01\x06\x0D\x00\x00\x00\x00\xAB\x65\x00\x00\x01\x00', True]).start()
			Timer(1, inject_silkroad,[0xB074, b'\x02\x00', True]).start()
			# Timer(1.5,inject_joymax,[0x7046, struct.pack('I',id)+b'\x0C',True]).start()
			return True

def teleported():
	global energy
	energy = False
	quests = get_quests()
	for questID in quests:
		if quests[questID]['completed']:
			notice('Pending Quest!')
			break
	if get_zone_name(get_character_data()['region']) == 'Diebesstadt':
		stop_bot()
		moveToBandit()
		# inject_joymax(0x7034, b'\x00\x6C\x6B\x01\x00',True)
		# Timer(4,inject_joymax,[0x7045,struct.pack('I',31),True]).start()
		# Timer(4,inject_joymax,[0x7034,b'\x00\x6C\x6B\x01\x00',True]).start()
		# Timer(4.5,inject_joymax,[0x7045,struct.pack('I',31),True]).start()

def moveToBandit():
	x1 = 9113
	y1 = 876
	x2 = get_position()['x']
	y2 = get_position()['y']
	dis = ((x2-x1)**2+(y2-y1)**2)**1/2
	if dis < 30:	
		talkToBandit()
		return	
	move_to(x1,y1,0)
	Timer(0.5,moveToBandit).start()

button1 = QtBind.createButton(gui, 'global_chat', 'Global', 530, 27)
text = QtBind.createLineEdit(gui,"",220,25,300,20)

def global_chat():
	phBotChat.Global(QtBind.text(gui,text))

def exitBandit():
	if not get_party():
		for i,x in enumerate(get_inventory()['items']):
			if x and i > 13:
				if x['name'] == 'Bandit Den Return Scroll':
					if x['quantity'] > 10:
						npcs = get_npcs()
						for id, npc in npcs.items():
							if "Diebesstadt" in npc['name']:
								inject_joymax(0x705A, struct.pack('I',id)+b'\x01',True)
					else :
						notice('BANDIT SCROLLS!')
					return

def script(arg):
	stop_bot()
	log(get_config_dir().replace('Config','Scripts')+arg[1]+'.txt')
	set_training_script(get_config_dir().replace('Config','Quests')+arg[1]+'.txt')
	start_bot()
	return
	
def droping():
	drops = get_drops()
	global dropg
	if len(drops) < 5:
		gold_available = get_character_data()['gold']
		gold = 100000000
		gold_minimo = 1000000
		if dropg:
			if gold_available > gold_minimo:
				droped = gold_available%gold
				if droped == 0:
					droped = gold
				Packet = b'\x0A'
				Packet += struct.pack('<I', droped)
				Packet += b'\x00\x00\x00\x00'
				inject_joymax(0x7034, Packet, False)
				Timer(0.5, droping).start()
			else:
				dropg = ~dropg
	else:
		Timer(0.5, droping).start()

def dropItem(name):
	global drop
	log('dropItem')
	for i,item in enumerate(get_inventory()['items']):
		if drop and item and i>12:
			if name.upper() in item['name'].upper():
				log(item['servername'])
				Packet = bytearray()
				Packet.append(0x07)
				Packet.append(i)
				inject_joymax(0x7034, Packet, True)
				Timer(0.5,dropItem,[name]).start()
				return
	drop = False

eventos = ['Lucky','Bargain']
stats = True

def easyPick(k=0):
	temp = False
	drops = get_drops()
	if k == 0:
		pets = get_pets()
		if pets:
			for k, v in pets.items():
				if v['type'] == 'pick':
					break
	if drops:
		for dropID in drops:
			if drops[dropID]['can_pick'] and 'lottery' in drops[dropID]['name'].lower():
				if k != 0:
					inject_joymax(0x70C5, struct.pack('I', k) + b'\x08' + struct.pack('I', dropID), False)
				inject_joymax(0x7074, b'\x01\x02\x01' + struct.pack('I', dropID), False)
				Timer(0.3,easyPick,[k]).start()
				log(drops[dropID]['name'])
				return
		for dropID in drops:
			if drops[dropID]['can_pick'] and 'immortal' in drops[dropID]['name'].lower():
				if k != 0:
					inject_joymax(0x70C5, struct.pack('I', k) + b'\x08' + struct.pack('I', dropID), False)
				inject_joymax(0x7074, b'\x01\x02\x01' + struct.pack('I', dropID), False)
				Timer(0.3,easyPick,[k]).start()
				log(drops[dropID]['name'])
				return
		for dropID in drops:
			if drops[dropID]['can_pick'] and drops[dropID]['name'] == 'Magic POP Card':
				if k != 0:
					inject_joymax(0x70C5, struct.pack('I', k) + b'\x08' + struct.pack('I', dropID), False)
				inject_joymax(0x7074, b'\x01\x02\x01' + struct.pack('I', dropID), False)
				Timer(0.3,easyPick,[k]).start()
				log(drops[dropID]['name'])
				return
		for dropID in drops:
			if drops[dropID]['can_pick'] and drops[dropID]['name'] == 'Reverse Reverse Return Scroll':
				if k != 0:
					inject_joymax(0x70C5, struct.pack('I', k) + b'\x08' + struct.pack('I', dropID), False)
				inject_joymax(0x7074, b'\x01\x02\x01' + struct.pack('I', dropID), False)
				Timer(0.3,easyPick,[k]).start()
				log(drops[dropID]['name'])
				return
		for dropID in drops:
			if drops[dropID]['can_pick'] and drops[dropID]['name'] == 'Global chatting':
				if k != 0:
					inject_joymax(0x70C5, struct.pack('I', k) + b'\x08' + struct.pack('I', dropID), False)
				inject_joymax(0x7074, b'\x01\x02\x01' + struct.pack('I', dropID), False)
				Timer(0.3,easyPick,[k]).start()
				log(drops[dropID]['name'])
				return
		for dropID in drops:
			if drops[dropID]['can_pick'] and drops[dropID]['name'] == 'Gold':
				if k != 0:
					inject_joymax(0x70C5, struct.pack('I', k) + b'\x08' + struct.pack('I', dropID), False)
				inject_joymax(0x7074, b'\x01\x02\x01' + struct.pack('I', dropID), False)
				Timer(0.3,easyPick,[k]).start()
				log(drops[dropID]['name'])
				return
			

def handle_joymax(opcode, data):
	global partyNumber
	global UniqueAlert
	global UINT
	global USTR
	global stats
	# if opcode == 0x706D:
	# 	name = struct.unpack_from('<' + str(data[6]) + 's',data,8)[0].decode('cp1252')
	# 	notice('0x706D: ' + name)
	# 	phBotChat.Party('Hello ['+name+']')
	# 	mobs = get_monsters()
	# 	for mobID in mobs:
	# 		if mobs[mobID]['type'] == 24:
	# 			phBotChat.Party(name + ' Here! => ['+mobs[mobID]['name'] +']')
	# 			break
	if opcode == 0x3864 and data:
		if struct.unpack_from('<s', data, 0)[0] == b'\x02':
			name = struct.unpack_from('<' + str(data[6]) + 's',data,8)[0].decode('cp1252')
			# notice('0x3864: ' + name)
			# phBotChat.Party('Hello ['+name+']')
			mobs = get_monsters()
			for mobID in mobs:
				if mobs[mobID]['type'] == 24:
					phBotChat.Party(name + ' Here! => ['+mobs[mobID]['name'] +']')
					break
	elif stats and opcode == 0x3153:
		Silk = str(struct.unpack_from('<I', data, 0)[0])
		SP = str(struct.unpack_from('<I', data, 4)[0])
		msg = get_character_data()['name'] + ' =>   SP: '+ SP + '     Silk: ' + Silk
		log(msg)
		threading.Thread(target=sendTelegram, args=[msg],).start()
		stats = False
		return True
	elif opcode == 0x30CF: #Mensajes de eventos
		if data == b'\x15\x02\x55\x00\x59\x6F\x75\x20\x6D\x75\x73\x74\x20\x63\x6F\x6D\x70\x6C\x65\x74\x65\x20\x74\x68\x65\x20\x63\x61\x70\x74\x63\x68\x61\x20\x76\x65\x72\x69\x66\x63\x61\x74\x69\x6F\x6E\x20\x74\x6F\x20\x70\x72\x6F\x63\x65\x65\x64\x20\x77\x69\x74\x68\x20\x62\x75\x79\x69\x6E\x67\x2F\x73\x65\x6C\x6C\x69\x6E\x67\x20\x74\x72\x61\x64\x65\x20\x67\x6F\x6F\x64\x73\x2E': # Trader Sell
			deleteClean()
		if get_character_data()['name'] == 'Seven':
			msg = str(data[4:])[2:-1]
			if 'Specifications' not in msg:
				if 'Search & Destroy' in msg or 'Horse Race' in msg or 'Lucky Global' in msg:
					threading.Thread(target=sendTelegram, args=[msg],).start()
				elif 'Be the first' in msg:
					log(msg)
					msg = msg.replace('Be the first to find and kill "[GM] Serapis" around ','`')+'`'
					notice(msg.replace('`',''))
					threading.Thread(target=sendTelegram, args=[msg],).start()
	elif opcode == 0xB069 and partyNumber != 0: #Party Form
		log((' '.join('{:02X}'.format(x) for x in data)))
		if data[0] != 2:
			log('xdxd')
			pt = str(struct.unpack_from('<I', data, 1)[0])
			log('Party number: ' + pt)
			if partyNumber != '0' and int(pt) < int(partyNumber):
				Packet = bytearray()
				Packet += struct.pack('<I', struct.unpack_from('<I', data, 1)[0])
				inject_joymax(0x706B, Packet, True)
			else:
				phBotChat.Guild('pe:0')
				# phBotChat.Private('Cuantica', 'pt:'+pt)
				if pt == partyNumber:
					threading.Thread(target=sendTelegram, args=[get_character_data()['name'] + ' -> Ganador'],).start()
	elif opcode == 0x7074: #quest mob count
		log(str(struct.unpack_from('<I', data, 1)[0]))
	elif opcode == 0x300C: # Unique Spawn
		if data[0] == 5:
			uniqueName = get_monster(struct.unpack_from('<I', data, 2)[0])['name']
			log(uniqueName)
			if UniqueAlert and (uniqueName in uniques or 'STR' in uniqueName) and get_character_data()['name'] == 'Seven':
				play_wav('Sounds/Unique.wav')
				threading.Thread(target=sendTelegram, args=[uniqueName],).start()
			elif USTR and 'STR' in uniqueName:
		 		play_wav('Sounds/Unique.wav')
		 		threading.Thread(target=sendTelegram, args=[uniqueName],).start()
		 		# phBotChat.Global('Merikh (STR) 663')
			elif UINT and 'INT' in uniqueName:
				log('xd')
				play_wav('Sounds/Unique.wav')
				threading.Thread(target=sendTelegram, args=[uniqueName],).start()
		elif data[0] == 6:
			name = str(data[8:])[2:-1]
			easyPick()
			log(name + ' Killed  -> '+ get_monster(struct.unpack_from('<I', data, 2)[0])['name'])
			# inject_joymax(0xA451, b'\x01', True)
			if QtBind.text(gui,uniqueSTRname) != '' and QtBind.text(gui,uniqueSTRname).lower() in get_monster(struct.unpack_from('<I', data, 2)[0])['name'].lower():
				log('EJECUTANDO SCRIPT DE CAMBIO')
				Timer(10,afterUnique).start()
	elif opcode == 0x3080: #SERVER_GAME_PETITION_REQUEST exchange
		if data[0] == 1:
			inject_joymax(0x3080,b'\x01\x01',False)
	elif opcode == 0x30D5: #Kill quest Mob
		log('quest mob')
		if struct.unpack_from('<I', data, 6)[0] == 50401285:
			log('Priest: ' + str(struct.unpack_from('<I', data, 40)[0]))
			if struct.unpack_from('<I', data, 40)[0] == 250 and 'Harsa' not in get_training_area()['path']:
				changeTrainingArea('Harsa')
		elif struct.unpack_from('<I', data, 6)[0] == 33624069:
			log('Harsa: ' + str(struct.unpack_from('<I', data, 40)[0]))
			if struct.unpack_from('<I', data, 40)[0] == 300 and 'Keisas' not in get_training_area()['path']:
				changeTrainingArea('Keisas')
		elif struct.unpack_from('<I', data, 6)[0] == 16846853:
			log('Keisas: ' + str(struct.unpack_from('<I', data, 40)[0]))
			if struct.unpack_from('<I', data, 40)[0] == 299:
				quest_complete()
			elif struct.unpack_from('<I', data, 40)[0] == 300 and 'Priest' not in get_training_area()['path']:
				changeTrainingArea('Priest')
	elif opcode == 0x751A: #FGW
		packet = data[:4] # Request ID
		packet += b'\x00\x00\x00\x00' # unknown ID
		packet += b'\x01' # Accept flag
		inject_joymax(0x751C,packet,False)
	return True

def afterUnique():
	useSpecialReturnScroll()
	set_profile(QtBind.text(gui,configName))
	start_bot()

def job():
	if get_inventory()['items'][8]:
		log('Hay capa')
		if get_zone_name(get_position()['region']) == 'Western-China-Donwhang':
			set_profile('Grinding')
			inject_joymax(0x7061, bytearray(), False)
			Packet = bytearray()
			Packet.append(0x00)
			Packet.append(0x08)
			Packet.append(0x10)
			Packet.append(0x00)
			Packet.append(0x00)
			inject_joymax(0x7034, Packet, False)
		Timer(15, job).start()
	else:
		log('No hay capa')
		npcs = get_npcs()
		Timer(0.5, move_to,[3548,2071,-106]).start()
		Timer(1, move_to,[3546,2086,-106]).start()
		for id, npc in npcs.items():
			if "Daily Quest Manager Shadi" in npc['name']:
				Timer(2,inject_joymax,[0x7045,struct.pack('I',id)+ b'\x00',False]).start() #Seleccionar NPC
				Timer(3,inject_joymax,[0x7046,struct.pack('I',id)+ b'5\x00\x02',False]).start() #Hablar con NPC
				Timer(4,inject_joymax,[0x30D4, b'\x08',False]).start() #Seleccionar Quest Templo
				Timer(5,inject_joymax,[0x30D4,b'\x05',False]).start() #Aceptar
				# Timer(6,phBotChat.All,['DWJG']).start()
				Timer(6, move_to,[3548,2071,-106]).start()
				Timer(7,start_bot).start()


def quest_complete():
	if get_quests()[1046]['completed']:
		stop_bot()
		useSpecialReturnScroll()
		Timer(1, job).start()
	else:
		Timer(1, quest_complete).start()

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
	inject_joymax(0x70C6, struct.pack('I', k), False)
	Timer(1,deleteClean).start()


def TerminarTransporte():
	DismountTransport()
	p = get_position()
	pX = random.uniform(-2,2)
	pY = random.uniform(-2,2)
	pX = pX + p['x']
	pY = pY + p['y']
	threading.Thread(target=move, args=(pX,pY,p['z'])).start()
	log('Movido')
	Timer(2.0, TerminationTransport,).start()
	Timer(2.5, inject_joymax,[0x705A, b'\x01\x00\x00\x00\x01' , True]).start()

def handle_silkroad(opcode,data):
	global PICK
	global partyNumber
	global targetBol
	global energy
	if opcode == 0x2002 and checkParty() and get_character_data()['name'] == 'Seven':
		pickWithPet()
		return True
	if opcode == 0x706D:
		partyNumber = struct.unpack_from('<I', data, 0)[0]
		notice(str(partyNumber))
	elif opcode == 0xA691 and data == b'\x36\x23\x00\x00':
		joinParty()
		return False
	elif opcode == 0xA691 and data == b'\x3A\x23\x00\x00':
		targetBol = not targetBol
		targetGeneral()
		return False
	elif opcode == 0x3091: #esencia1
		if data ==  b'\x00':
			trigerESSENCE()
			return False
		elif data == b'\x06':
			trigerESSENCE2()
			return False
		elif data ==  b'\x01':
			PICK = True
			threading.Thread(target=pick_loop).start()
			return False
		elif data ==  b'\x04':
			threading.Thread(target=picky).start()
			return False
		elif data ==  b'\x03':
			pickWithPet()
			return False
			# followUnique()
		elif data ==  b'\x02':
			followUnique()
			return False
	elif opcode == 0x7402:
		energy = not energy
		if energy:
			notice('Energia Activada')
		else:
			notice('Energia Desactivada')
		useEnergy()
	return True

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

def targetHunter():
	mobs = get_monsters()
	for mobID in mobs:
		if 'Hunter' in mobs[mobID]['name'] and mobs[mobID]['hp'] != 0:
			Packet =  struct.pack('i', mobID)
			Packet += b'\x00'
			inject_joymax(0x7045, Packet, True)
			Timer(0.5,targetHunter).start()
			return


def notice(message):
	p = struct.pack('B',7)
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x3026,p,False)


UniqueAlert = False
UniqueStart = False
GMCheck = QtBind.createCheckBox(gui,'CheckGM','GM Notify',10,130)
UniqueCheck = QtBind.createCheckBox(gui,'UniqueCh','Unique',10,70)
UniqueStartSheck = QtBind.createCheckBox(gui,'UniqueStartSwitcher','Unique Start',70,70)
gSTR = QtBind.createCheckBox(gui,'UniqueSTR','STR',30,90)
gINT = QtBind.createCheckBox(gui,'UniqueINT','INT',30,110)
QtBind.setChecked(gui, UniqueCheck, UniqueAlert)
QtBind.setChecked(gui, UniqueStartSheck, UniqueStart)
QtBind.setChecked(gui, GMCheck, True)
GMDisconnect = QtBind.createCheckBox(gui,'GMDC','GM DC',10,150)
GM_Alert = False
GM_DC = False
QtBind.setChecked(gui, gSTR, USTR)

def UniqueStartSwitcher(checked):
	global UniqueStart
	UniqueStart = checked

def UniqueSTR(checked):
	global USTR
	USTR = checked

def UniqueINT(checked):
	global UINT
	UINT = checked

def UniqueCh(checked):
	global UniqueAlert
	UniqueAlert = checked

def handle_event(t, data):
	global UniqueAlert
	global GM_DC
	global partyAlert
	if t == 9 and get_zone_name(get_character_data()['region']) not in ignoreZones:
		play_wav('Sounds/GM.wav')
		log(data)
		# if GM_DC:
			# Disconected()
		if GM_Alert and data not in ignore:
			player = get_character_data()
			name = player['name']
			zona = ' | '+str(get_zone_name(get_position()['region']))
			xy = ' | ' +str(int(player['x']))+','+str(int(player['y']))
			play_wav('Sounds/GM.wav')
			threading.Thread(target=sendTelegram, args=[name + ' -> ' + data + zona + xy],).start()
	elif t == 7:
		log(data)
		if get_character_data()['level'] < 11:
			Timer(1, inject_joymax, [0x3053, b'\x02', True]).start()
	elif t == 5:
			# play_wav('Sounds/Fiu.wav')
			# log(str(get_item(int(data))['name']))
		threading.Thread(target=sendTelegram, args=['*'+get_character_data()['name'] + '* -> `'+get_item(int(data))['name']+'`'],).start()
	elif t == 0 and UniqueAlert and '(INT)' not in data and 'Apis' not in data and 'Priest of Luck' not in data:
		play_wav('Sounds/Unique In Range.wav')
		notice(data)
		if partyAlert:
			phBotChat.Party('Here ---> ['+ data + ']')
		cancelAlchemy()
		log('xddd')
		goUnique()
	elif t == 8:
		quitarDressLucky()
	# elif t == 6 and not get_party(): #EVENT_ITEM_DROP 
	# 	pickWithPet()

def petScroll(arg = 0):
	i = 0
	for x in get_inventory()['items']:
		if x:
			if x['name'] == 'Red Wolf Summon Scroll Skin Scroll':
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0xEC)
				Packet.append(0x09)
				inject_joymax(0x704C, Packet, True)
				break
		i+=1
	return False

def CheckGM(checked):
	global GM_Alert
	GM_Alert = checked

def GMDC(checked):
	global GM_DC
	GM_DC = checked

def Notificar(checked):
	global TelegramBol
	TelegramBol = checked

def partyAlertChecker(checked):
	global partyAlert
	partyAlert = checked


btnReturn	= QtBind.createButton(gui,'SELL','SELL',250,65)
btnLast		= QtBind.createButton(gui,'Last','Last Recall Point',250,100)
DROP1GOLD	= QtBind.createButton(gui,'DROPXD','DROPGOLD',250,250)
clockBtn	= QtBind.createButton(gui,'resPet','CLOCK',600,210)
pickBTN		= QtBind.createButton(gui,'pick_function','PICK',600,240)
testing		= QtBind.createButton(gui,'testinger','TEST',250,280)

def testinger():
	npcs = get_npcs()
	for id, npc in npcs.items(): #recibe un elixir y un item en el pet de carga
		if "gestohlener Waren" in npc['name']:
			# p = b'\x01\x11'+ struct.pack('i', getWolf()) + b'\x05\x00\x00\x00\x00\x6A\x08\x00\x00\x90\x01\x03\x00\x4F\x69\x65'
			inject_joymax(0x7045, struct.pack('I',id), False) #Selecciona NPC
			Timer(0.5, inject_silkroad,[0xB034, b'\x01\x06\x0D\x00\x00\x00\x00\xAB\x65\x00\x00\x01\x00', True]).start() #Adv Elixir
			Timer(1, inject_silkroad,[0xB074, b'\x02\x00', True]).start()
			# Timer(1,inject_silkroad,[0xB034, p, True]).start() #Injecta la merca en el pet
			Timer(1.5,inject_joymax,[0x7046, struct.pack('I',id)+b'\x0C',True]).start() #Opcion para vender la merca
			return True

	
def checkParty():
	Party = get_party()
	if Party and get_character_data()['name'] == 'Seven':
		for memberID in Party:
			if Party[memberID]['region'] == get_character_data()['region'] and Party[memberID]['name'] != 'Seven':
				return False
	return True


def pickWithPet():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['type'] == 'pick':
				drops = get_drops()
				if drops:
					for dropID in drops:
						inject_joymax(0x70C5, struct.pack('I', k) + b'\x08' + struct.pack('I', dropID), False)
						Timer(0.5,pickWithPet).start()
						return
			return


def quitarInvisible():
	global PICK
	return PICK
			

def pick_function():
	global PICK
	PICK = not PICK
	pick_loop()

targetBol = False

def targetGeneral():
	global targetBol
	if targetBol:
		log('targeting generaling')
		mobs = get_monsters()
		for mobID in mobs:
			if mobs[mobID]['type'] == 0 and mobs[mobID]['hp'] != 0:
				x1 = get_position()['x']
				y1 = get_position()['y']
				max_distance = 0
				for mobID in mobs:
					if mobs[mobID]['type'] < 2 and mobs[mobID]['hp'] != 0:
						x2 = mobs[mobID]['x']
						y2 = mobs[mobID]['y']
						dis = ((x2-x1)**2+(y2-y1)**2)**1/2
						if max_distance == 0:
							max_distance = dis
							mobID_MAS_CERCANO = mobID
						elif dis < max_distance:
							max_distance = dis
							mobID_MAS_CERCANO = mobID
				inject_joymax(0x7045, b''+ struct.pack('<I', mobID_MAS_CERCANO), False)
				Timer(0.1,targetGeneral).start()
				return

def quitarDressLucky():
	items = enumerate(get_inventory()['items'])
	for slot, item in items:
		if item:
			if item['name'] == 'Arabian - Black Edition Dress (M)':
				log(item['name'])
				inject_joymax(0x7034, b'\x23\x00\x16', False)
				inject_joymax(0x7034, b'\x24' + struct.pack('I', slot) + b'\x00', False)
				Timer(0.5,quitarDressLucky).start()
				return
	items = enumerate(get_inventory()['items'])
	for slot, item in items:
		if item:
			if item['name'] == 'Samurai Accessory (M)':
				log(item['name'])
				inject_joymax(0x7034, b'\x24' + struct.pack('I', slot) + b'\x01', False)
				Timer(0.5,quitarDressLucky).start()
				return
	if get_inventory()['items'][13]:
		if get_inventory()['items'][13]['name'] == 'Global chatting':
			start_bot()
	return

def questHWT():
	quests = get_quests()
	for questID in quests:
		if quests[questID]['name'] == 'Collecting Pharaoh Tomb Heart (Beginner)':
			if quests[questID]['objectives'][0]['progress'] == 4:
				log('casi')
			break

def picky():
	drops = get_drops()
	if drops:
		for dropID in drops:
			x1 = get_position()['x']
			y1 = get_position()['y']
			max_distance = 0
			for dropID in drops:
				x2 = drops[dropID]['x']
				y2 = drops[dropID]['y']
				dis = ((x2-x1)**2+(y2-y1)**2)**1/2
				if max_distance == 0:
					max_distance = dis
					dropID_MAS_CERCANO = dropID
				elif dis < max_distance:
					max_distance = dis
					dropID_MAS_CERCANO = dropID
			inject_joymax(0x7074, b'\x01\x02\x01' + struct.pack('I', dropID_MAS_CERCANO), False)
			log('Agarrando Drop...')
			Timer(0.5,picky).start()
			return
	


def resPet():
	for i, item in enumerate(get_inventory()['items']):
		if item and i > 13:
			if 'Clock of Reincarnation' in item['name']:
				Packet = bytearray()
				Packet.append(i)
				Packet+= b'\xED\x66'
				for i, item in enumerate(get_inventory()['items']):
					if item and i > 13:
						if 'Flinke' in item['name'] or 'Monkey Summon Scroll' in item['name']:
							Packet.append(i)
							inject_joymax(0x704C, Packet, True)
							Timer(0.5,resPet).start()
							return



def uniqueHP():
	log('uniqueHP')
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['type'] != 24:
			# log(str(mobs[mobID]['hp']))
			log(str(mobs[mobID]['max_hp']))
			# log(str(round(mobs[mobID]['hp']/mobs[mobID]['max_hp'],2)))
			# phBotChat.Party('HP: '+str(round(mobs[mobID]['hp']/mobs[mobID]['max_hp'],2)*100)+'%')
			return

def getlog():
	log("\n+++"+str(get_log())+'+++')



def SELL():
	pets = get_pets()
	if pets:
		for petID in pets:
			if pets[petID]['type'] == 'transport':
				for i, item in enumerate(pets[petID]['items']):
					if item != None:
						# Packet = bytearray(b'\x14\xF1\x4A\xED\x00')
						Packet = bytearray(b'\x14\x90\x0E\x14\x00')
						Packet.append(i)
						Packet += b'\x90\x01\x1B\x00\x00\x00'
						inject_joymax(0x5624, Packet, True)
						log(str(get_character_data()['gold']))
						sleep(0.5)
						threading.Thread(target=SELL).start()
						break


def goUnique():
	log('goUnique')
	global UniqueStart
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['type'] == 24:
			x1 = mobs[mobID]['x']
			y1 = mobs[mobID]['y']
			move_to(x1,y1,0)
			if UniqueStart:
				set_training_position(0,x1,y1,0)
				log('iniciando bot por Unique')
				start_bot()
			x2 = get_position()['x']
			y2 = get_position()['y']
			dis = ((x2-x1)**2+(y2-y1)**2)**1/2
			if mobs[mobID]['name'] == 'Captain Ivy':
				p =  struct.pack('i', getWolf())
				p += b'\x02'
				p += struct.pack('i', mobID)
				inject_joymax(0x70C5, p, False)
				dis = dis-600
			if dis < 100:
				DismountHorse()
				return
	Timer(0.1,goUnique).start()

def getWolf():
	pets = get_pets()
	if pets:
		for pet, v in pets.items():
			if v['type'] == 'wolf':
				return pet	

def followUnique():
	mobs = get_monsters()
	for mobID in mobs:
		if mobs[mobID]['type'] == 24:
			move_to(mobs[mobID]['x'],mobs[mobID]['y'],0)
			Timer(1,followUnique).start()
	return

DROP = False

def DROPXD():
	global DROP
	DROP = ~DROP
	if DROP:
		DROP1()

def DROP1():
	global DROP
	if DROP:
		Packet = b'\x0A'
		Packet += struct.pack('<I', 1)
		Packet += b'\x00\x00\x00\x00'
		inject_joymax(0x7034, Packet, False)
		Timer(0.5,DROP1).start()

def ReturnScroll():
	Packet = b'\x7F\xAA\x00\x00\xB9\x0E\x00\x00'
	inject_joymax(0x715F, Packet, True)

def Last():
	Packet = b'\x7F\xAA\x00\x00\xD3\x0E\x00\x00\x02'
	inject_joymax(0x715F, Packet, True)
	
invisible = False
btn1 = QtBind.createButton(gui,'DismountTransport','DISMOUNT TRANSPORT',600,40)
btn1 = QtBind.createButton(gui,'DismountHorse','DISMOUNT HORSE',600,10)
btn2 = QtBind.createButton(gui,'MountTransport','MOUNT',600,70)
btn3 = QtBind.createButton(gui,'TerminationTransport','TERMINATE',600,100)
btn4 = QtBind.createButton(gui,'summonTradeHorse','SUMMON TRADER',600,130)
btn5 = QtBind.createButton(gui,'cancelReturnScroll','Cancelar Scroll',100,120)
# btn6 = QtBind.createButton(gui,'Disconected','DISCONECT',100,155)
btn7 = QtBind.createButton(gui,'useBanditScroll','Bandit Scroll',10,40)
btn8 = QtBind.createButton(gui,'DC','DC',10,170)
btn9 = QtBind.createButton(gui,'unequipJob','Unequip Job',250,160)
btn9 = QtBind.createButton(gui,'equipJob','Equip Job',250,190)
btn10 = QtBind.createButton(gui,'petScroll','Pet Scroll',600,160)
termbtm	= QtBind.createButton(gui,'TerminarTransporte','term',250,130)
termbtm1 = QtBind.createButton(gui,'spawnHorse','HORSE',600,190)

buscarMercabtn = QtBind.createButton(gui,'buscarMerca','buscarMerca',20,290)
Essences = QtBind.createButton(gui,'trigerESSENCE','ESSENCE',20,260)

superEssence = False
superEssence2 = False

def event_loop():
	global superEssence
	global superEssence2
	if superEssence:
		pets = get_pets()
		if pets:
			for petID in pets:
				if pets[petID]['name'] == 'Red Dragon':
					Strength = False
					Physical = False
					skills = get_active_skills()
					for skillID in skills:
						if skills[skillID]['name'] == 'Speed Essence':
							log('Eliminando Speed Essence')
							inject_joymax(0x7074, b'\x01\x05\x08\x85\x00\x00\x00', True)
						if skills[skillID]['name'] == 'Strength Essence':
							Strength = True
						elif skills[skillID]['name'] == 'Physical Damage Essence':
							Physical = True
					if not Strength:		
						inject_joymax(0xA691, b'\x33\x23\x00\x00', False)
					if not Physical:
						inject_joymax(0xA691, b'\x37\x23\x00\x00', False)
					break
	if superEssence2:
		pets = get_pets()
		if pets:
			for petID in pets:
				if pets[petID]['name'] == 'Red Dragon':
					Strength = False
					Speed = False
					skills = get_active_skills()
					for skillID in skills:
						if skills[skillID]['name'] == 'Physical Damage Essence':
							log('Eliminando Physical Damage Essence')
							inject_joymax(0x7074, b'\x01\x05\x06\x85\x00\x00\x00', True)
						if skills[skillID]['name'] == 'Speed Essence':
							Speed = True
						elif skills[skillID]['name'] == 'Strength Essence':
							Strength = True
					if not Speed:
						inject_joymax(0xA691, b'\x39\x23\x00\x00', False)
					if not Strength:		
						inject_joymax(0xA691, b'\x33\x23\x00\x00', False)
					break

def trigerESSENCE(n=0):
	global superEssence
	global superEssence2
	superEssence2 = False
	superEssence = not superEssence
	if superEssence:
		notice('Esencia Activada')
	else:
		notice('Esencia Desactivada')
	return True

def trigerESSENCE2(n=0):
	global superEssence2
	global superEssence
	superEssence = False
	superEssence2 = not superEssence2
	if superEssence2:
		notice('Esencia Activada')
	else:
		notice('Esencia Desactivada')

def ESSENCE():
	global superEssence
	if superEssence:
		pets = get_pets()
		if pets:
			for petID in pets:
				if pets[petID]['name'] == 'Red Dragon':
					Strength = False
					Physical = False
					skills = get_active_skills()
					for skillID in skills:
						if skills[skillID]['name'] == 'Strength Essence':
							Strength = True
						elif skills[skillID]['name'] == 'Physical Damage Essence':
							Physical = True
					if not Physical:
						inject_joymax(0xA691, b'\x37\x23\x00\x00', False)
					if not Strength:		
						inject_joymax(0xA691, b'\x33\x23\x00\x00', False)
					break
		Timer(1,ESSENCE).start()

def AtackPet():
	log('atacando')
	if atackSUNGSUNG:
		mobs = get_monsters()
		for mobID in mobs:
			if mobs[mobID]['name'] == 'Ghost SungSung':
				p =  struct.pack('i', getWolf())
				p += b'\x02'
				p += struct.pack('i', mobID)
				inject_joymax(0x70C5, p, False)
				break
		Timer(1,AtackPet).start()


def getWolf():
	pets = get_pets()
	if pets:
		for pet, v in pets.items():
			if v['type'] == 'wolf':
				# log(str(v))
				break
	return pet

def buscarMerca():
	global merca
	merca = not merca
	soundMerca()

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

def j0b():
	if get_zone_name(get_position()['region']) == 'Western-China-Donwhang':
		set_profile('Templo')
		inject_joymax(0x7061, bytearray(), False)
		Timer(2, DismountTransporte).start()
		Timer(3, equipJob).start()
		Timer(15, phBotChat.All,['::priest'],).start()
	else:
		Timer(1, j0b).start()

def unequipJob():
	Packet = bytearray()
	Packet.append(0x00)
	Packet.append(0x08)
	Packet.append(0x10)
	Packet.append(0x00)
	Packet.append(0x00)
	inject_joymax(0x7034, Packet, False)
	log('Quitando capa')

def equipJob():
	inventory = get_inventory()['items']
	for k, item in enumerate(inventory):
		if item and ('_THIEF_' in item['servername'] or '_TRADER_' in item['servername']):
			log(item['name'])
			Packet = bytearray()
			Packet.append(0x00)
			Packet.append(k)
			Packet.append(0x08)
			Packet.append(0x00)
			Packet.append(0x00)
			inject_joymax(0x7034, Packet, False)
			log('Poniendo capa')
			break

def DC():
	inject_joymax(0x704C, bytearray(), False)
	log('DC')
	return False

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

def chatpt(msg):
	phBotChat.Party(str(msg[1]))
	return False

def chat(msg):
	phBotChat.All(str(msg[1]))
	return False

def setTraining(script):
	log('Setting training script: ' + script[1])
	set_training_script('C:/Users/User/AppData/Local/Programs/phBot Testing/'+ str(script[1]) +'.txt')
	return False

def MountTransport():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['type'] == 'wolf' or v['type'] == 'transport':
				p = b'\x01'
				p += struct.pack('I', k)
				inject_joymax(0x70CB, p, False)
				log('mounted')
				return True
	return False

def DismountTransporte():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['mounted'] and v['type'] == 'wolf':
				log(v['type'])
				p = b'\x00'
				p += struct.pack('I', k)
				inject_joymax(0x70CB, p, False)
				log('dismounted')
				return True
	return False

def dismount():
	pets = get_pets()
	if pets:
		for slot, pet in pets.items():
			if pet['type'] == 'horse':
				p = b'\x00'
				p += struct.pack('I', slot)
				inject_joymax(0x70CB, p, False)
				Timer(0.5,dismount).start()
				break
	return

def DismountHorse():
	pets = get_pets()
	if pets:
		for slot, pet in pets.items():
			if pet['type'] == 'wolf':
				if pet['mounted']:
					log('is mounted')
					p = b'\x00'
					p += struct.pack('I', slot)
					inject_joymax(0x70CB, p, False)
					log('dismounted')
					Timer(1,DismountHorse).start()
					break
	return

def DismountTransport():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			log(v['type'])
			if v['type'] == 'horse':
				p = b'\x00'
				p += struct.pack('I', k)
				inject_joymax(0x70CB, p, False)
				log('dismounted')
				return True
	return False

def TerminatePet():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['type'] == 'wolf':
				p = struct.pack('I', k)
				p += b'\x03'
				inject_joymax(0x7116, p, False)
				log('terminamos')
				return True
	return False

def TerminationTransport():
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['type'] == 'transport':
				p = struct.pack('I', k)
				inject_joymax(0x70C6, p, False)
				log('terminamos')
				return True
	return False

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



def summonTradeHorse():
	inventory = get_inventory()
	items = inventory['items']
	for slot, item in enumerate(items):
		if item:
			if item['name'] == 'Donkey' or 'elephant' in item['name'].lower() or 'Goldclad Trade Horse' in item['name']:
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
				break
	return False

def mount(s):
	pets = get_pets()
	if pets:
		for k, v in pets.items():
			if v['type'] == 'wolf':
				p = b'\x01'
				p += struct.pack('I', k)
				inject_joymax(0x70CB, p, False)
				log('MOUNTED')
				return True
	return False

def SAM(s):
	inject_joymax(0x7059, b'\x07\x00\x00\x00', False)
	return False

def AN(s):
	inject_joymax(0x7059, b'\x06\x00\x00\x00', False)
	return False

def Disconected(k=1):
	log('disconected')
	Packet = bytearray()
	# inject_joymax(0x704C, Packet, False)
	log('Disconected')
	# Timer(1.0, os.kill, (os.getpid(), 9)).start()
	return False

def cancelReturnScroll():
	Packet = bytearray()
	inject_joymax(0x705B, Packet, False)
	log('Scroll cancelado')

# def equipJob(a=0):
# 	inventory = get_inventory()['items']
# 	for k, item in enumerate(inventory):
# 		if item and item['servername'].find('_THIEF_') > 0:
# 			log(item['name'])
# 			Packet = bytearray()
# 			Packet.append(0x00)
# 			Packet.append(k)
# 			Packet.append(0x08)
# 			Packet.append(0x00)
# 			Packet.append(0x00)
# 			inject_joymax(0x7034, Packet, False)
# 			Timer(2,log,('Equipando capa de thief'))
# 			break
# 	return False

def sendTelegram(data='quest'):
	url = 'https://api.telegram.org/bot6863881576:AAFjOYMaXdH_K_OBUnuDGaKNfJFkOQfoMgc/sendMessage?chat_id=149273661&parse_mode=Markdown&text='
	if '_' in data:
		url = 'https://api.telegram.org/bot6863881576:AAFjOYMaXdH_K_OBUnuDGaKNfJFkOQfoMgc/sendMessage?chat_id=149273661&text='
	url = url + urllib.parse.quote(data)
	urllib.request.urlopen(url,context=ssl._create_unverified_context())

def move(x,y,z):
	Timer(1.0, move_to,[x,y,z]).start()

def openStall(pid):
	inject_joymax(0x70B3, int(pid).to_bytes(4, 'little'), False)

# pid = QtBind.createLineEdit(gui,"",250,220,50,20)
# btn11 = QtBind.createButton(gui,'openStall','Open Stall',250,250)

def buyAll(i):
	if i < 10:
		log('Buying:' + str(i))
		Packet = bytearray()
		Packet.append(i)
		inject_joymax(0x70B4, Packet, False)
		Timer(1,buyAll,[i+1]).start()

def resurection(n):
	Packet = bytearray()
	Packet.append(n)
	Packet.append(0x00)
	Packet.append(0x00)
	Packet.append(0x00)
	inject_joymax(0x7059, Packet, False)

def help():
	global jelp
	if jelp:
		phBotChat.All('PARTY @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
		Timer(10,help).start()

def joinParty():
	global partyNumber
	if not get_party() and partyNumber != 0:
		Packet = bytearray()
		Packet += struct.pack('<I', partyNumber)
		inject_joymax(0x706D, Packet, False)
		Timer(5,joinParty).start()

# def test():
# 	global party
# 	if not get_party() and party:
# 		Packet = bytearray()
# 		Packet += struct.pack('<I', 123)
# 		inject_joymax(0x706D, Packet, False)

# def handle_joymax(opcode, data):
# 	global party
# 	if party and opcode == 0xB06D and data == b'\x02\x1C\x2C':
# 		party = False
# 	return True

def unequip(j,k):
	for i,item in enumerate(get_inventory()['items']):
		if item == None and i > j and k < 8:
			# log(str(i))
			# log(str(i)+': '+item['name'])
			Packet = bytearray()
			Packet.append(0x00)
			Packet.append(k)
			Packet.append(i)
			Packet.append(0x00)
			Packet.append(0x00)
			inject_joymax(0x7034, Packet, True)
			Timer(1,unequip,[i,k+1]).start()
			break

def equipItem(itemName):
	for i,item in enumerate(get_inventory()['items']):
		if item and i > 12:
			if itemName in item['name'].lower():
				log(item['name'])
				Packet = bytearray()
				Packet.append(0x00)
				Packet.append(i)
				Packet.append(0x06)
				Packet.append(0x00)
				Packet.append(0x00)
				inject_joymax(0x7034, Packet, True)
				break

def hunterAlarm():
	global NPC
	if NPC:
		pets = get_pets()
		if pets:
			for petID in pets:
				if pets[petID]['type'] == 'transport' and pets[petID]['items'][0] != None:
					mobs = get_monsters()
					for mobID in mobs:
						if mobs[mobID]['name'] == 'The Hunter':
							play_wav('Sounds/NPC.wav')
							Timer(40,hunterAlarm).start()
							return
					Timer(1,hunterAlarm).start()
					return
	NPC = ~NPC

def createParty():
	global partyNumber
	# log('createParty')
	# log(partyNumber)
	if partyNumber != '0':
		if get_inventory()['items'][8] == None:
			inject_joymax(0x7069, b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x01\x6E\x01\x00\x31' , True)
		else:
			inject_joymax(0x7069, b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x03\x01\x87\x08\x00\x42\x75\x73\x63\x61\x6E\x64\x6F' , True)
		Timer(5.1,createParty).start()

PICK = False

def handle_chat(t,player,msg):
	#1 All
	#2 Private
	#4 Party
	#5 Guild
	#6 Global
	#7 Notice
	#9 Stall
	global partyNumber
	global NPC
	global drop
	global dropg
	global superEssence
	global PICK
	if t == 2:
		foo = msg.split()
		for word in foo:
			if word.isnumeric():
				notice(word)
				partyNumber = int(word)
				break
	if msg == 'inter' and player == 'Seven':
		inject_joymax(0x705A, b'\x02\x00\x00\x00\x02\xA6\x00\x00\x00', False) #intermediate
	if msg == 'adv' and player == 'Seven':
		inject_joymax(0x705A, b'\x02\x00\x00\x00\x02\xA7\x00\x00\x00', False) #intermediate
	if player == 'Seven' and ' (STR)]' in msg and get_character_data()['name'] == 'Zoser':
		Party = get_party()
		if Party:
			for memberID in Party:
				if 'Seven' == Party[memberID]['name']:
					set_training_position(Party[memberID]['region'], Party[memberID]['x'], Party[memberID]['y'], 0.0)
					start_bot()
	if t == 6 and player == '[GA]Artyom' and get_character_data()['name'] == 'Seven':
		threading.Thread(target=sendTelegram, args=['`'+player+'`' + " -> " + msg],).start()
	if t == 2:
		play_wav('Sounds/PrivateMessage2.wav')
	if msg.isnumeric():
		notice(msg)
		partyNumber = int(msg)
		if t == 2 and player == 'Seven':
			joinParty()
	char = get_character_data()
	if t == 5 and msg[0:2] == '..' and get_character_data()['name'] != 'Trump' and get_character_data()['name'] != 'Seven':
		phBotChat.Global(msg[2:])
	elif t == 5 and msg == 'rand':
		point(get_position()['x'],get_position()['y'])
	elif t == 2 and player == 'Seven' and msg.lower() == 'donkey':
		inject_joymax(0x7034, b'\x18\x1B\x04\x04\x04\x0C\x19\x00\x50\x41\x43\x4B\x41\x47\x45\x5F\x49\x54\x45\x4D\x5F\x43\x4F\x53\x5F\x54\x5F\x44\x4F\x4E\x4B\x45\x59\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF4\x09\x00\x00', True)
	elif t == 2 and player == 'Seven' and msg.lower() == '50s':
		inject_joymax(0x7034, b'\x18\x1B\x04\x02\x00\x0D\x20\x00\x50\x41\x43\x4B\x41\x47\x45\x5F\x49\x54\x45\x4D\x5F\x4D\x41\x4C\x4C\x5F\x53\x43\x52\x4F\x4C\x4C\x5F\x53\x49\x4C\x4B\x5F\x35\x30\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x86\x06\x00\x00', True)
	elif msg == 'spawnhorse':
		spawnHorse()
	elif msg == 'zona':
		phBotChat.Private(player, get_zone_name(get_character_data()['region']))
	if t == 7:
		log('Noticia: '+msg)
	elif player == get_character_data()['name'] and msg == 'tptg':
		reverse_return(3, "Bandit-Bergfestung")
	elif player == get_character_data()['name'] and msg == 'tpdemon':
		reverse_return(3, "Heart Peak")
	elif player == get_character_data()['name'] and msg == 'tpuru1':
		reverse_return(3, "Black-Robber-Lager")
	elif player == get_character_data()['name'] and msg == 'tpuru2':
		reverse_return(3, "Tarimbecken")
	elif player == get_character_data()['name'] and msg == 'tplord1':
		reverse_return(3, "Niya-Ruine")
	elif player == get_character_data()['name'] and msg == 'tplord2':
		reverse_return(3, "Fruchtbarkeitstempel")
	elif player == get_character_data()['name'] and msg == 'tpisy1':
		reverse_return(3, "Alte Ruinen von Karakoram")
	elif player == get_character_data()['name'] and msg == 'tpisy2':
		reverse_return(3, "West-Karakoram")
	elif player == get_character_data()['name'] and msg == 'tpisy3':
		reverse_return(3, "Karakoram Cross Road")
	elif player == get_character_data()['name'] and msg == 'tproc':
		reverse_return(3, "Herzgipfel") #Wind Town
	elif player == get_character_data()['name'] and msg == 'tpivy':
		reverse_return(3, "Anatolian Plateau") #Wind Town
	elif player == get_character_data()['name'] and msg == 'tphwt':
		reverse_return(3, "Roter Boden") #Wind Town
	elif player == get_character_data()['name'] and msg == 'tpcerb':
		reverse_return(3, "Göttergarten") #Wind Town
	if (t == 4 or t == 2 or t == 1) and ',' in msg and msg.replace(',','').replace('-','').isnumeric():
			stop_trace()
			stop_bot()
			x = float(msg[0:msg.find(',')])
			y = float(msg[msg.find(',')+1:len(msg)])
			set_training_position(0, x, y, 0)
			if get_training_area()['radius'] == 0:
				set_training_radius(20)
			start_bot()
	elif msg.lower() == 'quest':
		log(str(get_quests()))
	elif msg[:3] == 'pe:':
		partyNumber = msg[3:]
		createParty()
	elif msg == '.dp' and player != char['name']:
		stop_bot()
		dropg = ~dropg
		Timer(0.5, droping).start()
	elif msg[:6] == "drop: " and char['name'] != player and char['job_name'] != player:
		log('xdasdasd')
		drop = True
		dropItem(msg[6:])
	elif msg.lower() == '.h':
		NPC = True
		hunterAlarm()
	elif msg.lower() == 'unequip':
		unequip(12,6)
	elif msg[:6] == 'equip:':
		equipItem(msg[7:])
	elif msg.lower() == 'dwht':
		Timer(0.5, move_to,[3548,2071,-106]).start()
		Timer(1, move_to,[3546,2086,-106]).start()
		def dwht():
			npcs = get_npcs()
			for id, npc in npcs.items():
				if "Donwhang" in npc['name']:
					inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x05\x00\x00\x00', False) #DWHT
					break
		Timer(2.5,dwht).start()
	elif msg.lower() == 'dwjg':
		Timer(0.5, move_to,[3548,2071,-106]).start()
		Timer(1, move_to,[3546,2086,-106]).start()
		def dwjg():
			npcs = get_npcs()
			for id, npc in npcs.items():
				if "Donwhang" in npc['name']:
					inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x01\x00\x00\x00', False) #DWJG
					break
		Timer(2.5,dwjg).start()
	elif msg.lower() == 'htdw':
		npcs = get_npcs()
		for id, npc in npcs.items():
			if "Hotan" in npc['name']:
				inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x02\x00\x00\x00', False) #HTDW
				break
	elif msg.lower() == 'htsk':
		npcs = get_npcs()
		for id, npc in npcs.items():
			if "Hotan" in npc['name']:
				inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x19\x00\x00\x00', False) #HTDW
				break
	elif msg.lower() == 'jgdw':
		npcs = get_npcs()
		for id, npc in npcs.items():
			if "Jangan" in npc['name']:
				inject_joymax(0x705A, struct.pack('I',id)+b'\x02\x02\x00\x00\x00', False) #JGDW
				break
	elif msg[:3].lower() =='pt:':
		inject_joymax(0x7061, bytearray(), False)
		partyNumber = int(msg[3:])
		Timer(1,joinParty).start()
	elif t == 5 and msg[:2] == '=>':
		set_profile(msg[2:])
	elif msg == ".90":
		inject_joymax(0x705A, b'\x1A\x00\x00\x00\x02\x0E\x01\x00\x00', True)
	elif msg == '.PT':
		global jelp
		jelp = ~jelp
		help()
	elif msg == '.p':
		inject_joymax(0x7069, b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x03\x01\x87\x08\x00\x42\x75\x73\x63\x61\x6E\x64\x6F' , True)
	elif msg == '.die':
		# inject_joymax(0x704B, b'\x97\x02\x00\x00', True)
		inject_joymax(0x705A, b'\x97\x02\x00\x00\x05\x03', True)
		# inject_joymax(0x705A, b'\x1A\x97\x02\x00\x00\x05\x03', True)
	elif msg.lower() == 'training':
		stop_trace()
		stop_bot()
		phBotChat.Party(str(set_training_script(get_training_area()['path'])))
		start_bot()
	elif msg[:2] == ': ':
		itemName = msg[2:]
		items = get_inventory()['items']
		for item in items:
			if item and itemName.upper() in item['name'].upper():
				phBotChat.Guild(item['name'] + ' [' + str(item['quantity']) + ']')
	elif msg.lower() == 'g':
		log('[Gold] '+str(get_character_data()['gold']))
	elif msg.lower() == '-g':
		log('[Gold] '+str(get_character_data()['gold']-1000000))
	elif (t == 2 or t == 1 or t == 4 or t == 5) and msg[0:2] == '::' and msg[3] != ' ':
		changeTrainingArea(msg[2:])
	elif msg.lower() == 'chatoff':
		global TelegramBol
		TelegramBol = False
		QtBind.setChecked(gui, NotificarCheck, False)
	elif msg == 'gmon':
		global GM_DC
		GM_DC = True
		QtBind.setChecked(gui, GMDisconnect, True)
	elif msg == 'gmoff':
		GM_DC = False
		QtBind.setChecked(gui, GMDisconnect, False)
	elif msg.lower() == 'getinv':
		items = get_inventory()['items']
		for i,item in enumerate(items):
			if item:
				log(item['name'] + ' :' +str(i))
	elif msg.lower() == 'getinv*':
		items = get_inventory()['items']
		for item in items:
			if item:
				log(item['servername'])
	# elif msg == '--':
	# 	i = 0
	# 	for x in get_inventory()['items']:
	# 		if x:
	# 			if 'Event Spotted Rabbit' in x['name']:
	# 				moveItem(i,1,'Event Spotted Rabbit')
	# 			elif 'Yellow Sparkle Ostrich Summon Scroll' in x['name']:
	# 				moveItem(i,2,'Yellow Sparkle Ostrich Summon Scroll')
	# 			elif 'HP Recovery Potion (XX-Large)' in x['name']:
	# 				moveItem(i,3,'HP Recovery Potion (XX-Large)')
	# 			elif 'MP Recovery Potion (XX-Large)' in x['name']:
	# 				moveItem(i,4,'MP Recovery Potion (XX-Large)')
	# 			elif 'Special Return Scroll' in x['name']:
	# 				moveItem(i,5,'Special Return Scroll')
	# 			elif 'Grass of life' in x['name']:
	# 				moveItem(i,6,'Grass of life')
	# 			elif 'HGP recovery potion' in x['name']:
	# 				moveItem(i,7,'HGP recovery potion')
	# 			elif 'Recovery kit (xx-large)' in x['name']:
	# 				moveItem(i,8,'Recovery kit (xx-large)')
	# 		i+=1
	elif msg == 'AS':
		resurection(2)
	elif msg == 'AN':
		resurection(3)
	elif msg == 'DW' or msg == 'HT':
		resurection(5)
	elif msg == 'CONS':
		# resurection(6)
		resurection(5)
	elif msg == 'SAM':
		resurection(7)
	elif msg == 'JG':
		resurection(13)
	elif msg.lower() == 'back':
		inject_joymax(0x3053, b'\x01', False)
	elif msg.lower() == 'zona':
		log(get_zone_name(get_position()['region']))
	elif msg.lower() == 'petoff':
		TerminatePet()
	elif msg.lower() == 'speed':
		useSpeed()
	# elif (t == 4 or t == 1 or t == 5) and msg == 'OFF':
	# 	Packet = bytearray()
	# 	Packet.append(0x03)
	# 	Packet.append(0x01)
	# 	inject_joymax(0x34BF, Packet, False)
	# 	log("EXP OFF")
	# elif (t == 4 or t == 1 or t == 5) and msg == 'ON':
	# 	Packet = bytearray()
	# 	Packet.append(0x03)
	# 	Packet.append(0x00)
	# 	inject_joymax(0x34BF, Packet, False)
	# 	log("EXP ON")
	# elif t == 9:
	# 	global Leaders
	# 	phBotChat.Private(player, 'Escribeme por WhatsApp a traves de este link https://wa.me/584123748436')
	# 	phBotChat.Private(player, 'Este es mi telefono +58 412 374 8436')
	if TelegramBol and player not in ignore and (t == 2 or t == 9):
		if player != char['name']:
			threading.Thread(target=sendTelegram, args=[player + " -> " + char['name'] + ' -> ' + msg],).start()
	if (t == 4 or t == 2) and msg.lower() == 'here' and char['name'] == player:
		char = get_character_data()
		x = int(char['x'])
		y = int(char['y'])
		phBotChat.Party(str(x)+','+str(y))
	elif (t == 1 or t == 2 or t == 4 or t == 5) and msg.lower() == 'stop':
		stop_trace()
		stop_bot()
		superEssence = False
		NPC = False
		drop = False
		dropg = False
		PICK = False
	elif t == 1 and msg == 'here':
		stop_bot()
		stop_trace()
		set_training_position(0, get_character_data()['x'], get_character_data()['y'], 0)
		start_bot()
	elif msg == 's' and char['name'] == player:
		stop_trace()
		start_bot()
	elif msg == 'd' and char['name'] == player:
		stop_bot()
		stop_trace()
	elif msg == 'set' and char['name'] == player:
		set_training_position(0, get_character_data()['x'], get_character_data()['y'], 0)
	elif msg.lower() == 'pet':
		spawnPet()
	elif msg.lower() == 'spawn':
		spawnThiefPet()()
	elif msg.lower() == 'leave':
		inject_joymax(0x7061, bytearray(), False)
	elif msg == '100%':
		manito100()
	elif msg == '60%':
		manito60()
	elif msg.lower() == 'scroll':
		useSpecialReturnScroll()
	elif msg == 'term':
		if t == 1 and (char['name'] == player or char['job_name'] == player):
			TerminarTransporte()
		elif t == 4 and char['name'] != player and char['job_name'] != player:
			TerminarTransporte()
	elif msg == 'cless' and (char['name'] == player or char['job_name'] == player) and get_client()['pid']:
		os.kill(get_client()['pid'], signal.SIGTERM)
		log('Client-less')
	elif msg == 'clientless' and char['name'] != player and char['job_name'] != player and get_client()['pid']:
		os.kill(get_client()['pid'], signal.SIGTERM)
		log('Client-less')
	elif t != 6 and msg == '2':
		DismountHorse()
		DismountTransport()
	elif t != 6 and msg == '1':
		MountTransport()
	elif t != 6 and msg == 'start':
		stop_trace()
		start_bot()
	elif t != 6 and msg == 'f':
		stop_bot()
		stop_trace()
		if char['name'] != player:
			start_trace(player)
	elif (t == 4 or t == 1 or t == 5) and msg[0] == 'r' and msg[1:].isnumeric() and len(msg[1:]) < 4:
		r = float(msg[1:len(msg)])
		set_training_radius(r)
	elif msg == 'usedevil':
		devil()
	elif msg == 'equipdevil':
		equipdevil()
	elif t == 2 and msg == 'pick':
		PICK = True
		pick_loop()
	elif char['name'] == player or char['job_name'] == player:
		if msg == '.os':
			phBotChat.All('s:'+ str(get_character_data()['player_id']))
	elif 's:' in msg[:2]:
		openStall(msg[2:])
	elif msg == '.buy':
		buyAll(0)
	elif msg == ';;' and player in myPlayers:
		log('superDC')
		inject_joymax(0x704C, bytearray(), False)
		os.kill(os.getpid(), 9)


def moveItem(i,k,name):
	# log(str(i))
	# log(str(len(get_inventory()['items'])-k))
	# log(get_inventory()['items'][i]['name'])
	# log(get_inventory()['items'][len(get_inventory()['items'])-k]['name'])
	# if not get_inventory()['items'][len(get_inventory()['items'])-k] or get_inventory()['items'][len(get_inventory()['items'])-k]['name'] != name:
	# if not get_inventory()['items'][len(get_inventory()['items'])-k] or get_inventory()['items'][i]['name'] == name:
	if i != len(get_inventory()['items'])-k:
		log('Moving: ' + name)
		Packet = bytearray()
		Packet.append(0x00)
		Packet.append(i)
		Packet.append(len(get_inventory()['items'])-k)
		Packet.append(get_inventory()['items'][i]['quantity'])
		Packet.append(0x00)
		inject_joymax(0x7034, Packet, True)
		Timer(2, moveItem,[i,k,name]).start()

def teleportacion(source,destination):
	t = get_teleport_data(source, destination)
	if t:
		npcs = get_npcs()
		for key, npc in npcs.items():
			if npc['name'] == source:
				inject_joymax(0x705A,struct.pack('<IBI', key, 2, t[1]),False)
			
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

def spawnPet():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if 'Dragon' in x['name']:
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0xCD)
				Packet.append(0x08)
				inject_joymax(0x704C, Packet, True)
				Timer(1,inject_joymax,[0xA691, b'\x33\x23\x00\x00', True]).start()
				break
		i+=1

def useSpeed():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if 'Drug' in x['name'] or x['name'] == 'Super Scroll (Schnelligkeit 100%)':
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0xEC)
				Packet.append(0x0E)
				inject_joymax(0x704C, Packet, True)
				break
		i+=1

def manito60():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if '60%' in x['name']:
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0xEC)
				Packet.append(0x26)
				inject_joymax(0x704C, Packet, True)
				break
		i+=1

def manito100():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if '100%' in x['name']:
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0xEC)
				Packet.append(0x26)
				inject_joymax(0x704C, Packet, True)
				break
		i+=1

def devil():
	Packet = bytearray()
	Packet.append(0x01)
	Packet.append(0x04)
	Packet.append(0xA5)
	Packet.append(0x79)
	Packet.append(0x00)
	Packet.append(0x00)
	Packet.append(0x00)
	inject_joymax(0x7074, Packet, False)

def equipdevil():
	i = 0
	for x in get_inventory()['items']:
		if x:
			if 'Devil' in x['name']:
				log(x['name'])
				Packet = bytearray()
				Packet.append(i)
				Packet.append(0x2D)
				Packet.append(0X0F)
				inject_joymax(0x704C, Packet, True)
				Packet = bytearray()
				Packet.append(0x24)
				Packet.append(i)
				Packet.append(0X04)
				inject_joymax(0x7034, Packet, True)
				break
		i+=1

def invisible():
	global invi
	return invi

def spawnHorse(a=0):
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

labelName = QtBind.createLabel(gui,'Nombre:',370,180)
scriptName = QtBind.createLineEdit(gui,"Scripts/",425,176,150,20)
labelXY = QtBind.createLabel(gui,'x,y :',363,147)
XY = QtBind.createLineEdit(gui,"",380,145,120,20)
MakeScript = QtBind.createButton(gui,'ScriptMaker',"MakeScript",410,220)
GetPosition = QtBind.createButton(gui,'GetPosition',"GetPosition",510,220)

uniqueSTRname = QtBind.createLineEdit(gui,"",325,276,80,20)
configName = QtBind.createLineEdit(gui,"Akeru",420,276,80,20)

def GetPosition():
	QtBind.setText(gui, XY, str(int(get_position()['x']))+','+str(int(get_position()['y'])))

def ScriptMaker():
	msg = QtBind.text(gui,XY)
	x = float(msg[:msg.find(',')])
	y = float(msg[msg.find(',')+1:])
	path = generate_path(x,y)
	file = open(QtBind.text(gui,scriptName)+'.txt','w')
	for k in path:
		s = 'walk,'+str(k[0])+','+str(k[1])+",0\n"
		file.write(s)
	file.close()
	log('Listo el script')

def changeTrainingArea(area):
	stop_trace()
	stop_bot()
	log(get_config_dir().replace('Config','Scripts')+area+'.txt')
	set_training_script(get_config_dir().replace('Config','Scripts')+area+'.txt')
	start_bot()

def joined_game():
	global UniqueAlert
	if get_character_data()['name'] == 'Seven':
		UniqueAlert = True
		QtBind.setChecked(gui, UniqueCheck, UniqueAlert)
		# Timer(2,joint).start()

def joint():
	global UniqueAlert
	if get_zone_name(get_character_data()['region']) != 'Rot Eggre':
		UniqueAlert = True
		QtBind.setChecked(gui, UniqueCheck, UniqueAlert)

if get_character_data()['name'] == 'Seven':
	UniqueAlert = True
	QtBind.setChecked(gui, UniqueCheck, UniqueAlert)

def pick_loop():
	set_training_position(0,0,0,0)
	stop_trace()
	stop_bot()
	global PICK
	if PICK:
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
							Timer(0.5, pick_loop).start()
						else:
							PICK = False
							useBanditScroll()
					else:
						spawnThiefPet()
						Timer(0.5, pick_loop).start()
					break
		else:
			log('No hay drops')
			PICK = False
			if thereIsATransport():
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
				dismount()
	return bol

def HayMerca(drops):
	response = False
	if drops:
		for dropID in drops:
			if 'TRADE' in drops[dropID]['servername']:
				return True
	return False

def recall(s):
	npcs = get_npcs()
	for id, npc in npcs.items():
		if "Donwhang" in npc['name']:
			inject_joymax(0x7059, struct.pack('I',id), False) #DWHT
			return True

def templo(s):
	npcs = get_npcs()
	for id, npc in npcs.items():
		if npc['name'] == 'Daily Quest Manager Shadi':
			Timer(0, inject_joymax,[0x7045, struct.pack('I',id), False]).start() #Seleccionar NPC
			Timer(0.5, inject_joymax,[0x7046, struct.pack('I',id) + b'\x02', False]).start() #Hablar con NPC
			Timer(1, inject_joymax,[0x30D4, b'\x08', False]).start() #Seleccionar Quest Templo
			Timer(1.5, inject_joymax,[0x30D4, b'\x05', False]).start() #Aceptar
			return True

def scrptChat(scriptName):
	stop_bot()
	useSpecialReturnScroll()
	set_training_script(get_config_dir().replace('Config','Scripts')+str(scriptName[1])+'.txt')
	Timer(3,start_bot).start()
	Timer(4,cancelReturnScroll).start()
	return True

log('[%s] Loaded' % __name__)
