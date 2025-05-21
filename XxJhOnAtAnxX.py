from phBot import *
import phBotChat
import urllib.request
from urllib.request import urlopen
import threading

token = urlopen('https://raw.githubusercontent.com/RahimSRO/Serapis/refs/heads/main/test.txt').read().decode("utf-8")[:-1]
TELEGRAM_ID = '149273661'
TELEGRAM_ID = '5987889810'

def handle_joymax(opcode, data):
	if opcode == 0x30CF and len(data) > 2:
		event = False
		data = str(data[4:])[2:-1]
		if isinstance(data, bytes):
			data = data.decode('ascii')
		elif not isinstance(data, str):
			data = str(data)
		if data.isascii() and 'Changelog' not in data and '2025.05.12' not in data:
			log(data)
		if 'Styria Clash' in data:
			event = True
		elif 'Last Man Standing' in data:
			event = True
		elif 'Zealots World' in data:
			event = True
		elif 'Roc will start' in data:
			event = True
		elif 'lucky global' in data.lower():
			event = True
		if event:
			threading.Thread(target=sendTelegram, args=[data],).start()
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

log('Event plugin v1.0 loeaded...')