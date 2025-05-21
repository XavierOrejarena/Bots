from phBot import *
import phBotChat
import urllib.request
from urllib.request import urlopen
import threading
import ssl
import struct

token = urlopen('https://raw.githubusercontent.com/RahimSRO/Serapis/refs/heads/main/test.txt').read().decode("utf-8")[:-1]
TELEGRAM_ID = '149273661'
TELEGRAM_ID = '5987889810'

ignore = ['(BANDIT)','Changelog','2025.05.12','with']

def handle_joymax(opcode, data):
	if opcode == 0x30CF and len(data) > 6 and get_character_data()['name'] == 'Zoser':
		event = False
		data = str(data)
		if 'Changelog' not in data and '2025.05.12' not in data and 'with' not in data and '(BANDIT)' not in data and 'item to plus' not in data:
			# log(data)
			if 'Styria Clash' in data:
				event = True
			elif 'Last Man Standing' in data:
				event = True
			elif 'Zealots World' in data:
				event = True
			elif 'Roc will start' in data:
				event = True
			elif 'Tower Defend' in data:
				event = True
			elif 'lucky global' in data.lower():
				event = True
			elif 'Survival Arena" event will start' in data:
				event =  True
			elif 'Search & Destroy" event will start' in data:
				event = True
			elif 'Alchemy" event will start' in data:
				event = True
			elif 'Roc' in data:
				event = True
			if event:
				data = str(data[4:])[2:-1]
				threading.Thread(target=sendTelegram, args=[data]).start()
	elif opcode == 0x300C and data[0] == 5: #unique spawn
		uniqueName = get_monster(struct.unpack_from('<I', data, 2)[0])['name']
		UNIQUES = ['Anubis','Isis','Selket','Neith','Beakyung The White Viper']
		if uniqueName in UNIQUES:
			threading.Thread(target=sendTelegram, args=[uniqueName]).start()
		log(uniqueName)
	return True

def sendTelegram(data='quest'):
	if data[0] == 'sendTelegram':
		data = 'quest'
	url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id=149273661&parse_mode=Markdown&text='
	if '_' in data:
		url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={TELEGRAM_ID}&text='
	url = url + urllib.parse.quote(data)
	urllib.request.urlopen(url,context=ssl._create_unverified_context())
	return True

def handle_chat(t,player,msg):
	if t == 2:
		threading.Thread(target=sendTelegram, args=[player + " -> " + char['name'] + ' -> ' + msg]).start()

log('Event plugin v0.1.0 loeaded...')