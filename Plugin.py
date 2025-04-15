from phBot import *

log('Ahora el plugin by Rahim es privado... Incluye auto FGW por 10k')
version = '0.1.0'
 
white_list = ['Space']

def handle_chat(t,player,msg):
	if is_whitelisted():
		if msg == 'tlp':
			tlp()

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

log(f'[FGW Plugin v{version} by Rahim]')
