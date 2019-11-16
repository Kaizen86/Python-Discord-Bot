import json #for parsing command permission configs

class EmptyConfigFileError(Exception):
    pass
class ConfigFileError(Exception):
    pass

def loadGeneralConfig(key):
	try:
		with open('bot.config') as json_data:
			config = json.load(json_data)
			return config[key]
	except:
		raise ConfigFileError("Unable to open bot.config")
		
def loadAdmins():
	admins = []
	try:
		for line in open("admins.config").readlines():
			line = line.replace("\n","")
			if line.split() == [] or line.startswith("#"):
				continue
			else:
				admins.append(line)
		if len(admins) == 0:
			raise EmptyConfigFileError("ERROR! No admins are defined in admins.config! Aborting...")
		return admins
	except:
		raise ConfigFileError("Unable to open admins.config")
		
def loadCommandPerms():
	try:
		with open('commands.config') as json_data:
			config = json.load(json_data)
			return config
	except:
		raise ConfigFileError("Unable to open commands.config")
