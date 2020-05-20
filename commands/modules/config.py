import json #for parsing command permission configs

class EmptyConfigFileError(Exception):
    pass
class ConfigFileError(Exception):
    pass

def loadAdmins():
    """Parses the admins.config file and returns an array of user ids."""
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

def loadConfigFile(filename, key=None):
    """Parses a json .config file from the specified filename.
    Either returns the entire parsed JSON or a specific value if a key is also provided."""
    try:
        with open(filename) as json_data:
            config = json.load(json_data)
            if not key:	return config
            else: return config[key]
    except:
        raise ConfigFileError(F"Unable to open {filename}")
