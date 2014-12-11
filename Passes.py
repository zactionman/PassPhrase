#! /usr/bin/python3

# This module is responsible for maniging all internal data relating
# to services/passwords and their related info. The idea is to keep
# this data in an easily pickleable format.

import pickle
import subprocess
import os.path as f

class Phrase():

	def __init__(self):
		
		self.Phrases = { 'Services' : [] }
	
	def Add(self, Serv, Log, Passwd, *args):
		# Add a entry to the Phrases dict.
		# Key is service name and value is a list of related info
		self.Phrases['Services'].append(Serv)

		self.Phrases[Serv] = [Log, Passwd]
		for answer in args:
			self.Phrases[Serv].append(answer)

	def Remove(self, Serv):
		# Get index for service name in Services list
		n = self.Phrases['Services'].index(Serv)
		# Delete service from service list
		del self.Phrases['Services'][n]
		# Delete related service info
		del self.Phrases[Serv]

	def Save(self, saveobj, savepath, enckey=None):
		if enckey == None:
			fil = open(savepath, 'wb')
			pickle.dump(saveobj, fil)
			fil.close()
		else:
			fil = open(savepath, 'wb')
			pickle.dump(saveobj, fil)
			fil.close()
			subprocess.call(['./cryptos', 'e', savepath, enckey])

	def Open(self, openpath, enckey=None):
		if enckey == None:
			fil = open(openpath, 'rb')
			loadfile = pickle.load(fil); return loadfile
			fil.close()
		else:
			subprocess.call(['./cryptos', 'd', openpath, enckey])
			fil = open('./.words', 'rb')
			loadfile = pickle.load(fil); return loadfile
			fil.close()
			subprocess.call(['./cryptos', 'c', './.words', 'keystub'])
		

