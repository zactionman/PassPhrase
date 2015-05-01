#! /usr/bin/python
# Begin translation to python script

from sys import argv
from subprocess import call
import os.path as f


# Do the actual encryption/decrypting
def crypton(TYPE, FILE, PASS=''):
    ENCRYP = FILE + '.enc'

    if TYPE == 'e' and f.isfile(FILE):
        status = call(['openssl', 'aes-256-cbc', '-a', '-salt', '-in', FILE, '-out', ENCRYP, '-pass', 'pass:{}'.format(PASS)])
        call(['rm', FILE])
    elif TYPE == 'd' and f.isfile(ENCRYP):
        call(['openssl', 'aes-256-cbc', '-d', '-a', '-in', ENCRYP, '-out', FILE, '-pass', 'pass:{}'.format(PASS)])
    elif TYPE == 'c' and f.isfile(FILE):
        call(['rm', FILE])
    else:
        print ('There was a problem with encryption/decryption')

if __name__ == '__main__':
    # Create appropriate variables
    SCRIPT = argv[0]
    TYPE, FILE = argv[1:3]
    # Only populate PASS if pass was given as an argument.  Otherwise empty string.
    if len(argv) == 4:
        PASS = argv[3]
    else:
        PASS = ''

    crypton(TYPE, FILE, PASS)
