#Authors note:
#This is one of the older remnants of the bot, made a few years ago.
#This was back when I was still learning (I still am) and as such
#it can be a bit hard to read. But it does work.

from bidict import bidict

class ShadowTranslator:
	def __init__(self):
		#define translations for each word, then convert the dictionary to be bidirectional
		rawdata = {
		"SA": "A",
		"BEH": "B",
		"NEK": "C",
		"DNE": "D",
		"BOH": "E",
		"COH": "F",
		"HON": "G",
		"GAI": "H",
		"HAIT": "I",
		"JAI": "J",
		"NAI": "K",
		"ELM": "L",
		"MES": "M",
		"KEN": "N",
		"SO": "O",
		"PLE": "P",
		"DAE": "Q",
		"ROU": "R",
		"QUES": "S",
		"REN": "T",
		"NUOH": "U",
		"VEK": "V",
		"DAIN": "W",
		"XUEI": "X",
		"QUAL": "Y",
		"ZIIE": "Z",

		" ": " ", #Space
		}
		self.__translations__ = bidict(rawdata)

	def ConvertToShadow(self, phrase):
		string = ""
		for letter in phrase.upper():
			if letter == "":
				print("blank")
				string += "  " #spaces should be symbolised as two spaces in shadow

			try:
				string += self.__translations__.inv[letter] + " " #add the translated character with a space to separate shadow words
			except:
				string += letter #letter was not in lookup; it is probably punctuation

		return string
	def ConvertFromShadow(self, shadow):
		string = ""

		#guide to variable names:
		#words = english words in shadow as array
		#word = specific english word in shadow
		#letters = list of shadow words as array
		#letter = individual shadow word

		words = shadow.split("   ")
		for word in words:
			letters = word.split()
			for letter in letters:
				foundpunctuation = []
				#if any punctuation is found in a shadow letter, we need to remove it for the lookup then add it back later.
				for character in letter:
					if not character.isalnum():
						#make a note
						foundpunctuation.append(character)
						#remove from string
						letter = letter.replace(character,"")
				try:
					for character in foundpunctuation: #add punctuation back
						string += character
					string += self.__translations__[letter] #add the translated character
				except:
					if not letter.isalpha(): #check for punctuation
						string += "?" #unknown character
			string += " " #spaces between words
		return string
