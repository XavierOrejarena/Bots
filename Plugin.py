from phBot import *
import phBotChat
from time import sleep
import re
from pathlib import Path
import urllib.request
import struct
from threading import Timer

bol = True
players = ['chapito01','chapito02']

def handle_chat(t,player,msg):
	global bol

	if t == 7 and bol and 'CONTROL BOT' in msg and name in players and Path(__file__).stem == '1auhASa1vckjbw2he-AS21FSADs':
		data = re.findall(r'\d+', msg)
		a = int(data[0])
		b = int(data[1])
		c = int(data[2])

		if msg.find('mas') < 0:
			result = a-b
		else:
			result = a+b

		result = result*c
		log(msg)
		log(str(result))
		# sleep(4)
		phBotChat.All(str(result))

def handle_event(t, data):
	name = get_character_data()['name']
	if t == 9 and name in players and Path(__file__).stem == '1auhASa1vckjbw2he-AS21FSADs':
		log(data)
		play_wav('C:/Users/Maximilians/AppData/Local/Programs/phBot Testing/sounds/GM.wav')
		url = 'https://api.telegram.org/bot1221990015:AAG2J37JO_AE2fUtmV1FKMj1y1MHCfF3C90/sendMessage?chat_id=774088349&text='
		url = url + urllib.parse.quote(name + " -> " + data)
		with urllib.request.urlopen(url) as f:
			print(f.read(300))

log("************************* Sell Merca *************************")

from phBot import *
import struct
from threading import Timer

from phBot import *
import struct
from threading import Timer

def handle_chat(t,player,msg):
	bol = False
	name = get_character_data()['name']
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
	phBotChat.Private('Nelliel1123','#'+x[1])
	log('Teleport chat Command')
	return 0

def scroll(x):
	phBotChat.Private('Nelliel1123','scroll')
	return 0

log("************************* Teleport Chat Command *************************")