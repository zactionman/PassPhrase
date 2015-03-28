#! /usr/bin/python3

# This module is responsible for maniging all internal data relating
# to services/passwords and their related info. The idea is to keep
# this data in an easily pickleable format.

import pickle
import subprocess
import os.path as f
from time import localtime as localt
from sys import argv

class Phrase():
    """An object containing all internal password data and methods for managing this data
    
    The primary purpose of this class is to maintain a the Phrases dictionary which contains
    an entry for each service (and their associated data) and a list of all known services
    which is kept in parallel.  The Phrases dict contains all important internal data and
    the subsequent methods modify this dictionary appropriately.

    For each added service the service name is appended to the 'Services' list.  Then
    a subsequent list (tied to a key that is equal to the service name) is added to the
    dict which contains all data in relation to that service in the following order:

    Login, Password, A1, A2, A3, A4, A5, Mod

    (A1-A5 is Answer1-Answer5 for any related questions for the account and Mod is
    modification time)
    """

    def __init__(self):
        
        # Main data object
        self.Phrases = { 'Services' : [] }
        
        # Get path to cryptos script
        # This will eventually change as I will eventually re-write cryptos in python
        self.crypton = argv[0][:-10] + 'cryptos'
        # Get user's home folder
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

    
    def Add(self, Serv, *args):
        """Add service(s) to the internal data structure (Phrases dict)"""

        # Make sure Service doesn't already exist
        if self.Phrases['Services'].count(Serv) == 0:
            # Add a entry to the Phrases dict.
            # Key is service name and value is a list of related info
            self.Phrases['Services'].append(Serv)

            # Create and popular a flat list of arguments (password data)
            apdata = []
            for answer in args:
                if type(answer) is list:
                    apdata.extend(answer)
                else:
                    apdata.append(answer)
            # Create internal list using listcomp
            self.Phrases[Serv] = [arg.strip('\n') for arg in apdata[:7]]
            # If list is less then seven add blank stuff
            while len(self.Phrases[Serv]) < 7:
                self.Phrases[Serv].append('')

            # Add time created/modified
            tim = localt(); mtm = ''
            mtim = str(tim[0]) + '/' + str(tim[1]) + '/' + str(tim[2])
            mtim = mtim + ' ' + str(tim[3]) + ':' + str(tim[4])
            self.Phrases[Serv].append(mtim)
            
            self.Phrases['Services'].sort()
            # Return added info for - incase calling frontend wants it...
            return [Serv] + self.Phrases[Serv]
            
        else:
            print ('This service already exists.  Please choose a unique service name')
            return None

    def Remove(self, *args):
        """Remove service(s) from internal data structure (Phrases Dict)"""

        for arg in args:
            if type(arg) is list:
                [self.Phrases['Services'].remove(serv) for serv in arg]
                [self.Phrases.__delitem__(serv) for serv in arg]
            else:
                self.Phrases['Services'].remove(arg)
                del self.Phrases[arg]
        # Get index for service name in Services list
        #n = self.Phrases['Services'].index(Serv)
        # Delete service from service list
        #del self.Phrases['Services'][n]
        # Delete related service info
        #del self.Phrases[Serv]


    def Modify(self, serv, *args):
        """Modify the contents of a service entry in the Phrases dict"""

        # Make sure Service exists
        if self.Phrases['Services'].count(serv) == 1:
            # Re-write service with modified data

            servdata = []
            # Expand/unpack args allowing use of combination of positional arguments/lists
            for data in args:
                if type(data) is list:
                    # If this is a list expand
                    servdata.extend(data)
                else:
                    # Single positional param gets appended
                    servdata.append(data)

            servdata = servdata[:7]

            # Add time modified
            tim = localt(); mtm = ''
            mtim = str(tim[0]) + '/' + str(tim[1]) + '/' + str(tim[2])
            mtim = mtim + ' ' + str(tim[3]) + ':' + str(tim[4])
            servdata.append(mtim)

            self.Phrases[serv] = servdata; return servdata
        else:
            print ("This service doesn't exist.  Please choose a unique service name")
            return None


    def Find(self, search, field='All'):
        """Find an entry based on a search string"""

        return [x for x in self.Phrases['Services'] if search in x]
                        

    def Save(self, saveobj, savepath, enckey=None):
        """Writeout internal data structure to picklefile then (optionally) encrypt it"""

        if enckey == None:
            # If no encryption key provided don't encrypt
            with open(savepath, 'wb') as fil:
                pickle.dump(saveobj, fil)
        else:
            # Pickle to file then encrypt file
            with open(savepath, 'wb') as fil:
                pickle.dump(saveobj, fil)
            subprocess.call([self.crypton, 'e', savepath, enckey])


    def Open(self, openpath, enckey=None):
        """Decrypt (optional) picklefile then load it into internal data structure.
        
        Phrase.Open needs to be called with the path of the file to be opened.  If
        the openpath is encrypted the encryption key needs to be passed as an argument
        as well.  If no encryption key is passed it will assume that the file is not
        encrypted.

        If the file is succesfully encrypted/opened then the pickle file will be loaded
        into the Self.Phrases dict (which is where all the internal dat is stored).  True
        will be returned so that any calling frontend can know that this was succesful.

        If the file does not exist or the encryption key is incorrect then any garbage
        files (resulting from bad decryption) will be cleaned and False will be returned so
        that any calling frontend can know that the data was not properly loaded.
        """

        try:
            if enckey == None:
                # If no encryption key provided assume that file is not encrypted
                with open(openpath, 'rb') as fil:
                    loadfile = pickle.load(fil)
            else:
                # Decrypt file then load it
                print ('Decrypting passwords to load into program')
                subprocess.call([self.crypton, 'd', openpath, enckey])
                with open(openpath, 'rb') as fil:
                    loadfile = pickle.load(fil)
                # Clean up the temporarily decrypted file
                print ('Clean temp file')
                subprocess.call([self.crypton, 'c', openpath, 'keystub'])
            self.Phrases = loadfile
            return True
        except pickle.UnpicklingError:
            print ('Typed in wrong encryption key')
            subprocess.call([self.crypton, 'c', openpath, 'keystub'])
            return False
        except FileNotFoundError:
            print ('File is encrypted, please type encryption key.')
            return False
        
    def Import(self, filnam, delim='\t'):
        """Import data from a field delimited text file"""

        # Open file for parsing
        with open(filnam, 'r') as impfil:
            # Keep track of services added
            added = []
            # Parse the file line by line and add stuff
            for line in impfil:
                # Split line into list
                ser = line.split(delim)
                # Add that data to the programs internal structures
                self.Add(ser[0], ser[1:])
                added.append(ser[0])
        # Return a list of added services to caller (So that the gui can add stuff to tree)
        return added


    def Export(self, filnam, delim='\t'):
        """Export data to a field delimited text file"""

        with open(filnam, 'w') as expfil:
            expfil.write("Password data sorted into the following fields separated by: '{}'\n".format(delim))
            expfil.write('Servicename Login Password Answer1 Answer2 Answer3 Answer4 Answer5\n\n')
            expfil.write('Password Data:\n')
            for serv in self.Phrases['Services']:
                curline = serv + delim + delim.join(self.Phrases[serv])
                expfil.write(curline + '\n')


