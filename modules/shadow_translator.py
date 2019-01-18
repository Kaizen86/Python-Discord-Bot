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
		self.__punctuation__ = ["¬","`","!","\"","£","$","%","^","&","*","(",")","_","-","=","+","[","]","{","}",";","'","#",":","@","~",",",".","/","\"","<",">","?","|","1","2","3","4","5","6","7","8","9","0"]
		
	def ConvertToShadow(self, phrase):
		string = ""
		for letter in phrase.upper():
			if letter is "":
				print("blank")
				string += "  " #spaces should be symbolised as two spaces in shadow
			
			try:
				string += self.__translations__.inv[letter] + " " #add the translated character with a space to separate shadow words
			except:
				if self.__punctuation__.__contains__(letter): #check for punctuation
					string += letter #add the character
				else:
					string += "?" #unknown character
						
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
				#if any punctuation is found in a shadow letter, we need to remove it for the lookup then add it back later.found
				for character in letter:
					if self.__punctuation__.__contains__(character):
						#make a note
						foundpunctuation.append(character)
						#remove from string
						letter = letter.replace(character,"")
				try:
					string += self.__translations__[letter] #add the translated character
				except:
					if foundpunctuation.__contains__(letter) == False: #check for punctuation
						string += "?" #unknown character
				for character in foundpunctuation: #add punctuation back
					string += character
			string += " " #spaces between words
		return string