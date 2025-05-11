from phBot import *
import phBotChat

def handle_chat(t,player,msg):
	msg = msg.lower()
	if msg == 'tlp':
		tlp()

def tlp():
	npcs = get_npcs()
	for id, npc in npcs.items():
		if npc['name'] == 'Dimensionslücke':
			log(npc['name'])
			inject_joymax(0x705A, struct.pack('I',id)+b'\x03\x00', False)
		if npc['name'] == '':
			log(npc['name'])
			inject_joymax(0x705A, struct.pack('I',id)+b'\x03\x00', False)

log('Teleport plugin loeaded!...')