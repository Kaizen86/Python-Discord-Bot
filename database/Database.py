from os import fsync
import json
import os.path

class Database:
	def __init__(self, filename):
		self._filepath = os.path.dirname(__file__) + "/" + filename
		try:
			# Attempt to load the file from disk
			with open(self._filepath, "r") as file:
				self._table = json.loads(file.read())  # Parse the file contents
		except:
			self._table = {}  # Either the file object had no/invalid contents or the file didn't exist. Make an empty dictionary!

	def save(self):
		"""Write the JSON table to the file"""
		with open(self._filepath, "w+") as file:
			json.dump(self._table, file)
			file.flush()  # Actually save it, please.
			fsync(file)  # This is not a suggestion. Save the bloody file.

	def read(self, key):
		"""Attempt to retrieve a value from the dictionary, returning None if non-existent"""
		key = str(key)
		if key not in self._table:
			return None
		return self._table[key]

	def write(self, key, value):
		"""Assign the value to the key in the dictionary"""
		self._table[str(key)] = value

def LoadAllFiles(bot):
	global guilds
	guilds = {}
	for guild in bot.guilds:
		guilds[guild.id] = Database("{}.json".format(guild.id))
