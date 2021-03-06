from phBot import *
import phBotChat
from time import sleep
import re
from pathlib import Path
import urllib.request
import struct
from threading import Timer
import os
import QtBind

gui = QtBind.init(__name__,'Super DC')
button1 = QtBind.createButton(gui, 'dc_traders', 'DC ALL TRADERS', 100, 120)

def dc_traders():
	phBotChat.Private('chapito01','.')
	phBotChat.Private('chapito02','.')
	phBotChat.Private('chapito03','.')
	phBotChat.Private('chapito04','.')


players = ['chapito01','chapito02','chapito03','chapito04','xTai','Xiomi','Tiranicuz','Sheon','Nelliel1123']
hunters = ['chapito01','chapito02','chapito03','chapito04','Nelliel1123','BLACKandBLUE','_Sophiia_','Mysophiia','chapito02']

def handle_chat(t,player,msg):
	global hunters
	name = get_character_data()['name']
	if msg == '.' and player in hunters and t == 2:
		if name == 'chapito01':
			phBotChat.Private('chapito02','.')
			phBotChat.Private('chapito03','.')
			phBotChat.Private('chapito04','.')
		Packet = bytearray()
		inject_joymax(0x704C, Packet, False)
		# sleep(1.0)
		Timer(1.0, os.kill, (os.getppid(), 9)).start()
		Timer(1.0, os.kill, (os.getpid(), 9)).start()
		# os.kill(os.getppid(), 9)
		# os.kill(os.getpid(), 9)
	global players
	bol = False
	if name == 'Nelliel1123' or name == 'BLACKandBLUE':
		if msg == '#1':
			source = 'Harbor Manager Marwa'
			destination = 'Pirate Morgun'
			bol = True
		elif msg == '#2':
			source = 'Tunnel Manager Topni'
			destination = 'Tunnel Manager Asui'
			bol = True
		if bol:
			teleport(source,destination)

	if t == 7 and 'CONTROL BOT' in msg and name in players and Path(__file__).stem == '1auhASa1vckjbw2he-AS21FSADs':
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

log("*** Sell Merca ***")

def handle_event(t, data):
	name = get_character_data()['name']
	if t == 9 and Path(__file__).stem == '1auhASa1vckjbw2he-AS21FSADs':
		log(data)
		play_wav('C:/Users/Maximilians/AppData/Local/Programs/phBot Testing/sounds/GM.wav')
		lru = '_LHuSAEVa7VbqI/sendMessage?chat_id=774088349&text='
		url = 'https://api.telegram.org/bot1221990015:AAHlL2X_NInc3xNo9MEnX' + lru
		url = url + urllib.parse.quote(name + " -> " + data)
		with urllib.request.urlopen(url) as f:
			print(f.read(300))

log("*** GM Alert ***")

def teleport(source,destination):
	t = get_teleport_data(source, destination)
	if t:
		npcs = get_npcs()
		for key, npc in npcs.items():
			if npc['name'] == source or npc['servername'] == source:
				log("Plugin: Selecting teleporter ["+source+"]")
				inject_joymax(0x7045, struct.pack('<I', key), False)
				Timer(2.0, inject_joymax, (0x705A,struct.pack('<IBI', key, 2, t[1]),False)).start()
				Timer(2.0, log, ("Plugin: Teleporting to ["+destination+"]")).start()
				return

def tlp(x):
	global hunters
	phBotChat.Private(x[1],x[2]+','+x[3])
	log('Teleported by Command')
	return 0

def msg(x):
	phBotChat.Private(x[1],x[2])
	log('Teleported by Command')
	return 0

def message(x):
	global hunters
	for k in hunters:
		phBotChat.Private(k,x[1])
	log('Message by Command')
	return 0

def scroll(x):
	phBotChat.Private('Nelliel1123','scroll')
	phBotChat.Private('BLACKandBLUE','scroll')
	log('Scrolled by Command')
	return 0

log("*** Teleport Chat Command ***")
