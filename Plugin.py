from phBot import *
import phBotChat
from time import sleep
import re
from pathlib import Path
import urllib.request
import struct
from threading import Timer

players = ['chapito01','chapito02']

def handle_chat(t,player,msg):
	log("XD")
	global players
	name = get_character_data()['name']

	if t == 7 and 'CONTROL BOT' in msg and name in players and Path(__file__).stem == '1auhASa1vckjbw2he-AS21FSADs':
		log("Maximiliano es gay")
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