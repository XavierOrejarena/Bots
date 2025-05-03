from phBot import *
import QtBind
import struct
from threading import Timer
import phBotChat
import urllib.request
import ssl
import time
import math

guiDimen = QtBind.init(__name__,'Dimen')

setProfile_Btn = QtBind.createButton(guiDimen,'spawn_dimension','Spawn Dimen',20,20)
talk_npc_Btn = QtBind.createButton(guiDimen,'talk_npc','Talk to NPC',20,50)
call_one_Btn = QtBind.createButton(guiDimen,'call_one_for_one','Call One For One',20,80)
tlp_Btn = QtBind.createButton(guiDimen,'tlp','Teleport',20,110)
start_Btn = QtBind.createButton(guiDimen,'start_stop','START/STOP',140,260)

distance = QtBind.createLineEdit(guiDimen,'320',100,200,150,20)
actualLine = QtBind.createLineEdit(guiDimen,'1',100,230,150,20)
actual  = int(QtBind.text(guiDimen,actualLine))
tiempo = [actual,time.time()]
start = False
n = 20
R = 35
lideres = ['Seven','Zoser','Norte','dCarnage']
for lider in lideres:
	if get_character_data()['name'] == lider:
		break
log(lider)
filename = 'Script.txt'
goUnique = True
murio_tierra = False
display = 0
mob_killed = 0
YUNO_SPAWNED = bytes.fromhex('1C 0C 02 1D 00 55 49 49 54 5F 53 54 54 5F 57 4F 52 53 48 49 50 5F 59 55 4E 4F 5F 53 50 41 57 4E 45 44')
JUPITER_SPAWNED = bytes.fromhex('1C 0C 02 20 00 55 49 49 54 5F 53 54 54 5F 57 4F 52 53 48 49 50 5F 4A 55 50 49 54 45 52 5F 53 50 41 57 4E 45 44')
PRIMERA_PUERTA_K16 = bytes.fromhex('1C 0C 01 16 00 55 49 49 54 5F 53 54 54 5F 4A 55 50 49 54 45 52 5F 41 5F 30 30 32')
SEGUNDA_PUERTA_K217 = bytes.fromhex('1C 0C 01 16 00 55 49 49 54 5F 53 54 54 5F 4A 55 50 49 54 45 52 5F 41 5F 30 30 33')
CUARTA_PUERTA_K247 = bytes.fromhex('1C 0C 01 16 00 55 49 49 54 5F 53 54 54 5F 4A 55 50 49 54 45 52 5F 41 5F 30 30 32')
QUINTA_PUERTA_K357 = bytes.fromhex('1C 0C 01 16 00 55 49 49 54 5F 53 54 54 5F 4A 55 50 49 54 45 52 5F 41 5F 30 30 35')
SEXTA_PUERTA_K380 = bytes.fromhex('1C 0C 01 16 00 55 49 49 54 5F 53 54 54 5F 4A 55 50 49 54 45 52 5F 41 5F 30 30 35')
TERCERA_PUERTA_K247 = bytes.fromhex('1C 0C 01 16 00 55 49 49 54 5F 53 54 54 5F 4A 55 50 49 54 45 52 5F 41 5F 30 30 34')

# data = bytes.fromhex('16 EF FA 06 89 A1 06 10 00 00 00 00 C2 52 18 00 00 00 00 00 00')
# data = bytes.fromhex('9D 99 FA 06 89 A1 06 10 00 00 00 00 C2 52 18 00 00 00 00 00 00')
# log(str(struct.unpack_from('I',data,4)[0]))#268870025


def start_stop():
	global start
	global tiempo
	global actual
	start = not start
	if start:
		log('Start')
		actual = int(QtBind.text(guiDimen,actualLine))
		tiempo[0] = actual
		tiempo[1] = time.time()
		start_bot()
	else:
		log('Stop')

def azulPerma(message):
	p = b'\x15\x04'
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x30CF,p,False)

def teleported():
	global murio_tierra
	global filename
	global lider
	if get_zone_name(get_character_data()['region']) == 'Anbetungshalle':
		Timer(4,delete_pet).start()
		stop_trace()
		if is_master():
			log('Soy master')
			urllib.request.urlopen('https://api.telegram.org/bot6863881576:AAHQ34H1cMzGz8XsNf5SqiCkY2wQ-dpBBG4/sendMessage?chat_id=149273661&parse_mode=Markdown&text=Dimension%20%20`'+get_character_data()['name']+'`',context=ssl._create_unverified_context())
			phBotChat.Party('~'+str(is_master()))
			Timer(1,move_to_npc,[19480,6425]).start()
		else:
			go_to_buff(32236,19480,6425,839)
			if get_character_data()['name'] == lider and murio_tierra:
				filename = 'Yuno.txt'
			if get_character_data()['name'] == lider:
				log('dire k en all en 20 seg')
				Timer(20,phBotChat.All,['k']).start()
	elif get_zone_name(get_character_data()['region']) == 'The Earths Raum':
		delete_pet()
		if get_character_data()['name'] == lider:
			go_to_buff(-32749,-20851,126,-134) #buff
			filename = 'Salir.txt'
			Timer(50,phBotChat.All,['k']).start()
			# go_to_buff(-32749,-20812,125,-134) #bug

def tlp():
	npcs = get_npcs()
	for id, npc in npcs.items():
		log(npc['name'])
		if npc['name'] == 'Dimensionslücke':
			log('Teleport a The Earth')
			Dismount()
			inject_joymax(0x705A, struct.pack('I',id)+b'\x03\x00', False)
		if npc['name'] == '':
			Dismount()
			inject_joymax(0x705A, struct.pack('I',id)+b'\x03\x00', False)

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

def call_one_for_one(slot,id):
	log('call_one_for_one')
	if slot < 8:
		Party = get_party()
		for i,memberID in enumerate(Party):
			if i == slot:
				log('calling: ' +str(slot))
				inject_joymax(0x751A, struct.pack('I',memberID), False)
				Timer(0.5,call_one_for_one,[slot+1,id]).start()
				return
	log('Exit NPC')
	inject_joymax(0x704B, struct.pack('L', id), False)
	set_training_position(0, 19480, 6425, 0)
	start_bot()

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
	log(str(dis))

def Dismount():
	pets = get_pets()
	for k, v in pets.items():
		if v['mounted']:
			log('Dismounting')
			inject_joymax(0x70CB, b'\x00'+struct.pack('I', k), False)
			return True

def handle_chat(t,player,msg):
	msg = msg.lower()
	global start
	global actual
	global tiempo
	global lider
	global goUnique
	global filename
	global murio_tierra
	global mob_killed
	global goUnique
	global R
	if msg[0] == '~' and t == 4 and msg[1:].isnumeric():
		Party = get_party()
		if Party:
			for memberID in Party:
				if memberID == int(msg[1:]):
					Dismount()
					log('Dismounted')
				else:
					return()
	elif msg == 'update!' and get_character_data()['name'] == player:
		name1 = 'Script'
		name2 = 'Yuno'
		name3 = 'Jupiter'
		name4 = 'Salir'

		descargar_txt(name1)
		descargar_txt(name2)
		descargar_txt(name3)
		descargar_txt(name4)
	# elif msg.isnumeric():
	# 	R = msg
	# 	red(f'R ahora es {R}')
	elif msg == 'talk'and is_master():
		phBotChat.Party('~'+str(is_master()))
		talk_npc()
	elif msg == 'file':
		log(filename)
	elif msg == 'spawn':
		lider = player
		goUnique = True
		mob_killed = 0
		filename = 'Script.txt'
		murio_tierra = False
		if is_master():
			spawn_dimension()
	elif msg == 'tlp':
		tlp()
	elif msg == 'fgw':
		lider = player
		FGW(player)
	elif msg == 'y' and get_character_data()['name'] != player:
		start_trace(player)
	elif msg == 'k':
		if get_character_data()['name'] != player:
			stop_bot()
			stop_trace()
			log('k start tracing to '+player)
			start_trace(player)
		else:
			start = not start
			if start:
				# actual = int(QtBind.text(guiDimen,actualLine))
				actual = 1
				tiempo[0] = actual
				tiempo[1] = time.time()
				start_bot()
			else:
				green(f'k = {str(actual)}')
				stop_bot()
	elif msg[0] == 'k' and msg[1:].isnumeric() and get_character_data()['name'] == player:
		start = True
		actual = int(msg[1:])
		tiempo[0] = actual
		tiempo[1] = time.time()
		start_bot()
	elif msg == 'm':
		log(str(get_monsters()))
		return
		mobs = get_monsters()
		if mobs:
			for mobID in mobs:
				if mobs[mobID]['hp'] != 0:
					x1 = mobs[mobID]['x']
					y1 = mobs[mobID]['y']
					x2 = get_position()['x']
					y2 = get_position()['y']
					dis = (((x2-x1)**2+(y2-y1)**2)**1/2)
					log(str(dis))
	elif msg == 'next':
		actual +=1
	elif msg == 'go!':
		goUnique = not goUnique
	elif msg == 'yuno':
		filename = 'Yuno.txt'
	elif msg == 'jupiter':
		filename = 'Jupiter.txt'
	elif msg == 'salir':
		filename = 'Salir.txt'


def is_master():
	Party = get_party()
	if Party:
		for memberID in Party:
			if get_character_data()['name'] == Party[memberID]['name']:
				return memberID
			else:
				return False
	return False

def event_loop():
	global start
	global actual
	global tiempo
	global filename
	global display
	if start:
		if display != actual:
			log(str(actual))
			display = actual
		x2 = get_position()['x']
		y2 = get_position()['y']
		poss = leer_linea_n(archivo=filename,numero_linea=actual)
		if '❌' in poss:
			log(f'No existe la linea... en {filename}')
			stop_bot()
			start = False
			return
		elif '/' in poss:
			azulPerma('Ejecutando comando...')
			poss = poss.split(',')
			if poss[0] == '/bard':
				Party = get_party()
				for memberID in Party:
					if Party[memberID]['name'] in poss:
						phBotChat.Private(Party[memberID]['name'],'scroll')
			elif poss[0] == '/chat':
				phBotChat.Party(poss[1])
			elif poss[0] == '/private':
				WARRIORS = ['How','Wan','Woke']
				Party = get_party()
				for memberID in Party:
					if Party[memberID]['name'] in WARRIORS:
						log(Party[memberID]['name'])
						log(poss[1])
						phBotChat.Private(Party[memberID]['name'],poss[1])
						break
			actual +=1
			tiempo[0] = actual
			tiempo[1] = time.time()
			return
		x1 = int(poss.split(',')[1])
		y1 = int(poss.split(',')[2])
		move_to(x1,y1,0)
		set_training_position(0,x1,y1,0)
		# log(f"moving to: {str(x1)},{str(y1)}")
		dis = ((x2-x1)**2+(y2-y1)**2)**1/2
		if dis < 2 and no_hay_mobs():
			actual +=1
			tiempo[0] = actual
			tiempo[1] = time.time()
		if time.time()-tiempo[1] > n and  dis < 2:
			phBotChat.Party('k')
			actual +=1
			azulPerma(f'Pasaron {n} seg...')
			phBotChat.Party(f'k{actual}')
		if tiempo[0] != actual:
			tiempo[0] = actual
			tiempo[1] = time.time()


def leer_linea_n(archivo="Script.txt", numero_linea=1):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            if 1 <= numero_linea <= len(lineas):
                return lineas[numero_linea - 1].rstrip('\n')
            else:
                return f"❌ El archivo solo tiene {len(lineas)} líneas. Línea {numero_linea} no disponible."
    except FileNotFoundError:
        return f"❌ El archivo '{archivo}' no se encontró."

def no_hay_mobs():
	mobs = get_monsters()
	if mobs:
		for mobID in mobs:
			if mobs[mobID]['hp'] != 0:
				x1 = mobs[mobID]['x']
				y1 = mobs[mobID]['y']
				x2 = get_position()['x']
				y2 = get_position()['y']
				dis = (((x2-x1)**2+(y2-y1)**2)**1/2)
				# log(str(dis))
				if dis < int(QtBind.text(guiDimen,distance)):
					return False
	return True

def delete_pet():
	log('delete_pet')
	pets = get_pets()
	if pets:
		for petID in pets:
			if pets[petID]['type'] == 'wolf':
				inject_joymax(0x7116, struct.pack('i',petID) + b'\x00', True)
				Timer(0.5,delete_pet).start()
				return

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
	log(str(dis))

# data = bytes.fromhex('9B F8 61 00 54 FE C9 10 00 00 00 00 70 7B 19 00 00 00 00 00 00')
# log(str(struct.unpack_from('I',data,4)[0]))


def handle_joymax(opcode, data):
	global tiempo
	global lider
	global filename
	global mob_killed
	global actual
	if opcode == 0x3056:
		tiempo[1] = time.time()
		if get_zone_name(get_character_data()['region']) == 'Anbetungshalle':
			mob_killed +=1
			log(f'Mobs: {mob_killed}')
			if struct.unpack_from('I',data,4)[0] == 281673300 and get_character_data()['name'] == lider:#268870025
				red(f'Murio Jupiter')
				log(f'Murio Jupiter')
				Timer(5,exitFGW).start()
				log((' '.join('{:02X}'.format(x) for x in data)))
				return True
				# mobID = struct.unpack_from('I',data,0)[0]
				# mob_name = get_monsters()[mobID]['name']
				# UNIQUES = ['The Earth','Yuno','Jupiter']
				# if mob_name in UNIQUES:
	elif opcode == 0x751A:
		packet = data[:4] # Request ID
		packet += b'\x00\x00\x00\x00' # unknown ID
		packet += b'\x01' # Accept flag
		inject_joymax(0x751C,packet,False)
	elif opcode == 0x300C:
		if data == YUNO_SPAWNED:
			azulPerma('Salio Yuno')
			earth()
		if get_character_data()['name'] == lider:
			if data == JUPITER_SPAWNED:
				azulPerma('Salio Jupiter')
				filename = 'Jupiter.txt'
				phBotChat.Party('stop')
				phBotChat.Party('true')
				phBotChat.Party('zerc')
				start_no_drop()
			elif 'UIIT_STT_JUPITER_A_' in str(data):
				azulPerma(f'Puerta: {str(data)[-4:-1]}')
				azulPerma(str(mob_killed))
				log(f'Puerta: {str(data)[-4:-1]} & {str(mob_killed)} actual: {actual}')
	elif opcode == 0x3068 and get_character_data()['name'] == lider: #party item droped distributed
		itemName = get_item(struct.unpack_from('<I', data, 4)[0])['name']
		playerName = get_party()[struct.unpack_from('<I', data, 0)[0]]['name']
		if struct.unpack_from('<I', data, 4)[0] > 33892 and struct.unpack_from('<I', data, 4)[0] < 33901:
			msg = f'item [{itemName}] is distributed to [{playerName}]'
			azulPerma(msg)
			sendTelegram(f'item `{itemName}` is distributed to `{playerName}`')
	elif opcode == 0xB034 and len(data) > 11 and get_character_data()['name'] == lider: #item gained
		dropType = struct.unpack_from('h', data, 0)[0]
		# log(str(dropType))
		if dropType == 7169 or dropType == 4353:
			itemID = get_item(struct.unpack_from('I', data, 11)[0])
			itemName = itemID['name']
			if struct.unpack_from('I', data, 11)[0] > 33892 and struct.unpack_from('I', data, 11)[0] < 33901:
				azulPerma(f'item [{itemName}] gained.')
				playerName = get_character_data()['name']
				sendTelegram(f'`{itemName}` Gained. ---> `{playerName}`')
		elif dropType == 1537:
			itemID = get_item(struct.unpack_from('I', data, 7)[0])
			itemName = itemID['name']
			if struct.unpack_from('I', data, 7)[0] > 33892 and struct.unpack_from('I', data, 7)[0] < 33901:
				azulPerma(f'item [{itemName}] gained.')
				playerName = get_character_data()['name']
				sendTelegram(f'`{itemName}` Gained. ---> `{playerName}`')
	elif opcode == 0x3057 and len(data) == 15 and get_zone_name(get_character_data()['region']) == 'Anbetungshalle' and struct.unpack_from('I',data,9)[0] == 0 and get_character_data()['name'] == lider:
		return True
		mobID = struct.unpack_from('I',data,0)[0]
		mob_name = get_monsters()[mobID]['name']
		UNIQUES = ['The Earth','Yuno','Jupiter']
		if mob_name in UNIQUES:
			red(f'Murio {mob_name}')
			exitFGW()
			log((' '.join('{:02X}'.format(x) for x in data)))
	return True

def sendTelegram(data='quest'):
	if data[0] == 'sendTelegram':
		data = 'quest'
	url = 'https://api.telegram.org/bot6863881576:AAHQ34H1cMzGz8XsNf5SqiCkY2wQ-dpBBG4/sendMessage?chat_id=149273661&parse_mode=Markdown&text='
	url = url + urllib.parse.quote(data)
	urllib.request.urlopen(url,context=ssl._create_unverified_context())
	return True

def FGW(lider):
	if get_character_data()['name'] == lider:
		phBotChat.Party(':>FGW')
		phBotChat.Party('stop')
		phBotChat.Party('scroll')
		phBotChat.Party('false')
		phBotChat.Party('r25')
		Party = get_party()
		WARRIORS = ['How','Wan','Woke']
		if Party:
			for memberID in Party:
				if Party[memberID]['name'] in WARRIORS:
					phBotChat.Private(Party[memberID]['name'],'r30')
					break
		Timer(5,FGW2).start()

def red(message):
	name = 'Rahim'
	data = b'\x42'+struct.pack('H', len(name))
	for word in name:
		data += word.encode('ascii')
		data += b'\x00'
	data += struct.pack('H', len(message))
	for word in message:
		data += word.encode('ascii')
		data += b'\x00'
	data += b'\x00\x00\xFF\xFF\xEC\xEB\x10\x01\x00'
	inject_silkroad(0x30CF,data,False)

def handle_event(t, data):
	global start
	global lider
	if t == 0 and get_zone_name(get_character_data()['region']) == 'Anbetungshalle':
		start = False
		green(f'Unique: {data}')
		if get_character_data()['name'] == lider:
			Timer(0.5,goJupiter).start()

def goJupiter():
	global goUnique
	if goUnique:
		mobs = get_monsters()
		if mobs:
			for mobID in mobs:
				if mobs[mobID]['type'] == 24:
					x2 = mobs[mobID]['x']
					y2 = mobs[mobID]['y']
					x1 = get_position()['x']
					y1 = get_position()['y']
					region = mobs[mobID]['region']
					move_to(x2,y2,0)
					dis = ((x2-x1)**2+(y2-y1)**2)**1/2
					if dis < 10:
						set_training_position(region,x1,y1,0)
					Timer(0.5,goJupiter).start()

def goYuno():
	log('goYuno')
	global goUnique
	global start
	global R
	if goUnique:
		mobs = get_monsters()
		if mobs:
			for mobID in mobs:
				if mobs[mobID]['type'] == 24:
					x2 = mobs[mobID]['x']
					y2 = mobs[mobID]['y']
					x1 = get_position()['x']
					y1 = get_position()['y']
					region = mobs[mobID]['region']
					dx = x1 - x2
					dy = y1 - y2
					distancia = math.sqrt(dx**2 + dy**2)
					dx /= distancia
					dy /= distancia
					x3 = x2 + dx * R
					y3 = y2 + dy * R
					set_training_position(region,x3,y3,0)
					move_to(x3,y3,0)
					Timer(1,goYuno).start()
					return

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

def exitFGW():
	log('exitFGW')
	if get_drops():
		Timer(1,exitFGW).start()
	else:
		phBotChat.All('scroll')
		phBotChat.All('stop')
		phBotChat.All(':>1')
		Timer(1,phBotChat.Party['f']).start()

def start_no_drop():
	if not get_drops():
		phBotChat.All('k')
		return
	Timer(1,start_no_drop).start()

def green(message):
	name = 'Rahim'
	data = b'\x42'+struct.pack('H', len(name))
	for word in name:
		data += word.encode('ascii')
		data += b'\x00'
	data += struct.pack('H', len(message))
	for word in message:
		data += word.encode('ascii')
		data += b'\x00'
	data += b'\x00\xFF\x00\xFF\xF1\x2C\x30\x01\x00'
	inject_silkroad(0x30CF,data,False)

def descargar_txt(name):
    try:
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/RahimSRO/Serapis/865db4031ef9007b7546cdca62b7ea630a61f7b6/{name}.txt', f'{name}.txt')
        log(f"Archivo guardado como: {name}.txt")
    except Exception as e:
        log(f"Error al descargar el archivo: {e}")

version = '1.0.0'
ver = QtBind.createLabel(guiDimen,'v'+version,690,300)
log(f'[Expert FGW v{version}] by Rahim]')