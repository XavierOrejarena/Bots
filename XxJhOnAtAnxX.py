from phBot import *
import phBotChat
import urllib.request
from urllib.request import urlopen
import threading
import ssl
import struct

token = urlopen('https://raw.githubusercontent.com/RahimSRO/Serapis/refs/heads/main/test.txt').read().decode("utf-8")[:-1]
TELEGRAM_ID = '149273661'
name = 'Seven'
TELEGRAM_ID = '5987889810'
name = 'BardBuff_2'

ignore = ['(BANDIT)','Changelog','2025.05.12','with']

def handle_joymax(opcode, data):
	if opcode == 0x30CF and len(data) > 6 and get_character_data()['name'] == name:
		event = False
		msg = str(data)
		if 'Changelog' not in msg and '2025.05.12' not in msg and 'with' not in msg and '(BANDIT)' not in msg and 'item to plus' not in msg and '100 Times' not in msg:
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
			elif 'lucky global' in msg.lower():
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
	if t == 2 and get_character_data()['name'] == name:
		threading.Thread(target=sendTelegram, args=[player + " -> " + get_character_data()['name'] + ' -> ' + msg]).start()

log('Event plugin v0.2.0 loeaded...')

# data = bytes.fromhex('15 01 1F 00 22 54 6F 77 65 72 20 44 65 66 65 6E 64 22 20 65 76 65 6E 74 20 68 61 73 20 65 6E 64 65 64 2E')
# data = bytes.fromhex('15 01 2E 00 22 50 76 50 20 4D 61 74 63 68 69 6E 67 22 20 65 76 65 6E 74 20 77 69 6C 6C 20 73 74 61 72 74 20 69 6E 20 31 30 20 6D 69 6E 75 74 65 73 2E')
# msg = str(data[4:])[2:-1]
# log(msg)