#! /usr/bin/python3

# This module is responsible for maniging all internal data relating
# to services/passwords and their related info. The idea is to keep
# this data in an easily pickleable format.

import pickle
import subprocess
import os.path as f
import random

class Phrase():

	def __init__(self):
		
		self.Phrases = { 'Services' : [] }
		
		home = f.expanduser('~')
		# Find any existing passwords files.  
		# If none exist create variable containing a path of where it will be written
		if f.isfile(home + '/.config/passphrase/words.enc') or f.isfile(
			home + '/.config/passphrase/words'):
			self.wfile = home + '/.config/passphrase/words'
		elif f.isfile(home + '/.passphrase/words.enc') or f.isfile(
			home + '/.passphrase/words'):
			self.wfile = home + '/.passphrase/words'
		elif f.isfile('.words.enc') or f.isfile('.words'):
			self.wfile = '.words'
		else:
			print ('\nNo previously created passwords. Starting with blank sheet')
			if f.isdir(home + '/.config'):
				self.wfile = home + '/.config/passphrase/words'
				if not f.isdir(home + '/.config/passphrase'):
					subprocess.call(['mkdir', home + '/.config/passphrase'])
			elif f.exists(home):
				self.wfile = home + '/.passphrase/words'
				if not f.isdir(home + '/.passphrase'):
					subprocess.call(['mkdir', home + '/.passphrase'])
			else:
				self.wfile = '.words'

	
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
			# If no encryption key provided don't encrypt
			fil = open(savepath, 'wb')
			pickle.dump(saveobj, fil)
			fil.close()
		else:
			# Pickle to file then encrypt file
			fil = open(savepath, 'wb')
			pickle.dump(saveobj, fil)
			fil.close()
			subprocess.call(['./cryptos', 'e', savepath, enckey])

	def Open(self, openpath, enckey=None):
		if enckey == None:
			# If no encryption key provided assume that file is not encrypted
			fil = open(openpath, 'rb')
			loadfile = pickle.load(fil); return loadfile
			fil.close()
		else:
			# Decrypt file then load it
			print ('Decrypting passwords to load into program')
			subprocess.call(['./cryptos', 'd', openpath, enckey])
			fil = open(openpath, 'rb')
			loadfile = pickle.load(fil)
			fil.close()
			# Clean up the temporarily decrypted file
			print ('Clean temp file')
			subprocess.call(['./cryptos', 'c', openpath, 'keystub'])
			return loadfile
		

