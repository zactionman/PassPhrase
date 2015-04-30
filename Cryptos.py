#! /bin/bash

# A basic little module to be called by the PassPhrase program to handle encryption
# and decryption. It should take either 'e' or 'd' as the first argument. 'e' tells
# it to encrypt and 'd' tells it to decrypt. The second argument is the file to
# encrypt/decrypt, and the third argument is the password for the cipher.

TYPE=$1
FILE=$2
PASS=$3

if [[ $TYPE == 'e' && -f $FILE ]]; then
	openssl aes-256-cbc -a -salt -in $FILE -out ${FILE}.enc -pass pass:$PASS
	rm $FILE
	exit 0
elif [[ $TYPE == 'd' && -f ${FILE}.enc ]]; then
	openssl aes-256-cbc -d -a -in ${FILE}.enc -out $FILE -pass pass:$PASS
	exit 0
elif [[ $TYPE == 'c' && -f $FILE ]]; then
	rm $FILE
	exit 0
else
	echo 'There was a problem with encryption/decryption' 1>&2
	exit 1
fi