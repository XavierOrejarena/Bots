from phBot import *
import phBotChat
import urllib.request
from urllib.request import urlopen
import threading
import ssl
import struct
import os
import signal

token = urlopen('https://raw.githubusercontent.com/RahimSRO/Serapis/refs/heads/main/test.txt').read().decode("utf-8")[:-1]
# TELEGRAM_ID = '149273661'
# name = 'Seven'
TELEGRAM_ID = '5987889810'
# name = 'BardBuff_2'

file = open('name.txt',mode='r')
name = file.read()
file.close()
ignore = ['(BANDIT)','Changelog','2025.05.12','with']

def handle_silkroad(opcode,data):
	if opcode == 0x7074:
		log('trying to clientless...')
		os.kill(get_client()['pid'], signal.SIGTERM)
	return

def handle_joymax(opcode, data):
	if opcode == 0x30CF and len(data) > 6 and get_character_data()['name'] == name:
		event = False
		msg = str(data)
		if 'Changelog' not in msg and '2025.05.12' not in msg and 'with' not in msg and '(BANDIT)' not in msg and 'item to plus' not in msg and '100 Times' not in msg and 'Temple' not in msg:
			# log(data)
			if 'Styria Clash' in msg:
				event = True
			elif 'Last Man Standing' in msg:
				event = True
			elif 'Zealots World' in msg:
				event = True
			elif 'Roc will start' in msg:
				event = True
			elif 'Tower Defend' in msg:
				event = True
			elif 'Lucky Global' in msg:
				event = True
			elif 'Survival Arena" event will start' in msg:
				event =  True
			elif 'Search & Destroy" event will start' in msg:
				event = True
			elif 'Alchemy" event will start' in msg:
				event = True
			elif 'Roc' in msg:
				event = True
			elif 'PvP Matching' in msg:
				event = True
			if event:
				log((' '.join('{:02X}'.format(x) for x in data)))
				msg = str(data[4:])[2:-1]
				threading.Thread(target=sendTelegram, args=[msg]).start()
	elif opcode == 0x300C and data[0] == 5 and get_character_data()['name'] == name: #unique spawn
		uniqueName = get_monster(struct.unpack_from('<I', data, 2)[0])['name']
		UNIQUES = ['Anubis','Isis','Selket','Neith','Beakyung The White Viper']
		if uniqueName in UNIQUES:
			threading.Thread(target=sendTelegram, args=[uniqueName]).start()
		log(uniqueName)
	# elif opcode == 0x3068 and get_character_data()['name'] in lideres: #party item droped distributed
	# 	itemName = get_item(struct.unpack_from('<I', data, 4)[0])['name']
	# 	playerName = get_party()[struct.unpack_from('<I', data, 0)[0]]['name']
	# 	if struct.unpack_from('<I', data, 4)[0] > 33892 and struct.unpack_from('<I', data, 4)[0] < 33901:
	# 		msg = f'item [{itemName}] is distributed to [{playerName}]'
	# 		azulPerma(msg)
	# 		sendTelegram(f'item `{itemName}` is distributed to `{playerName}`')
	elif opcode == 0xB034 and len(data) > 11: #item gained
		dropType = struct.unpack_from('h', data, 0)[0]
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
	return True

def sendTelegram(data='quest'):
	if data[0] == 'sendTelegram':
		data = 'quest'
	url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={TELEGRAM_ID}&parse_mode=Markdown&text='
	if '_' in data:
		url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={TELEGRAM_ID}&text='
	url = url + urllib.parse.quote(data)
	urllib.request.urlopen(url,context=ssl._create_unverified_context())
	return True

def handle_chat(t,player,msg):
	if t == 2:# and get_character_data()['name'] == name:
		threading.Thread(target=sendTelegram, args=[player + " -> " + get_character_data()['name'] + ' -> ' + msg]).start()

def handle_event(t, data):
	if t == 5:
		threading.Thread(target=sendTelegram, args=['*'+get_character_data()['name'] + '* -> `'+get_item(int(data))['name']+'`'],).start()

def azulPerma(message):
	p = b'\x15\x04'
	p += struct.pack('H', len(message))
	p += message.encode('ascii')
	inject_silkroad(0x30CF,p,False)


# chat_name = get_character_data()['name']
# if chat_name == name:
# else:
# 	log(f'char name: {chat_name}')
# 	log(f'file name: {name}')
log('Jhonatan Plugin v4.0 loeaded...')

# data = bytes.fromhex('15 01 1F 00 22 54 6F 77 65 72 20 44 65 66 65 6E 64 22 20 65 76 65 6E 74 20 68 61 73 20 65 6E 64 65 64 2E')
# data = bytes.fromhex('15 01 2E 00 22 50 76 50 20 4D 61 74 63 68 69 6E 67 22 20 65 76 65 6E 74 20 77 69 6C 6C 20 73 74 61 72 74 20 69 6E 20 31 30 20 6D 69 6E 75 74 65 73 2E')
# msg = str(data[4:])[2:-1]
# log(msg)