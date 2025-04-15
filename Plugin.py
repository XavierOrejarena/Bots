from phBot import *

log('Ahora el plugin by Rahim es privado... Incluye auto FGW por 10k')
version = '0.1.0'
 
white_list = ['Space']

def handle_chat(t,player,msg):
	if is_whitelisted():
		if msg == 'tlp':
			tlp()
			if get_character_data()['name'] == player:
				green('Teleported by Rahim.')

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

def is_whitelisted():
	global white_list
	Party = get_party()
	if Party:
		for memberID in Party:
			if Party[memberID]['name'] in white_list:
				return True
	else:
		if get_character_data()['name'] in white_list:
			return True
	return False

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

def Dismount():
	pets = get_pets()
	for k, v in pets.items():
		if v['mounted']:
			log('Dismounting')
			inject_joymax(0x70CB, b'\x00'+struct.pack('I', k), False)
			return True
			
log(f'[FGW Plugin v{version} by Rahim]')
