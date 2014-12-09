#! /usr/bin/python3

# This is the part of the PassPhrase program for managing the passphrases and their
# data internally

class Phrase():

	def __init__(self):
		
		self.Phrases = { 'Services' : [] }
	
	def Add(self, Serv, Log, Passwd, *args):
		
		self.Phrases['Services'].append(Serv)

		self.Phrases[Serv] = [Log, Passwd]
		for answer in args:
			self.Phrases[Serv].append(answer)

	def Remove(self, Serv):
		pass

		
