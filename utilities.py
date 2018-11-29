#!/usr/bin/python

from Crypto.Cipher import AES
from Crypto import Random
from os import stat
import random
import string 

def twos_comp(num,bit_length):
    if num < 0:
        num = (1 << bit_length) + num
    else:
        if (num & (1 << (bit_length - 1))) != 0:
            num = num - (1 << bit_length)
    return num

#get IV from encrypted byte array
def parse_IV(byte_arr):
    IV = byte_arr[:16]
    str_IV = str(IV)
    return str(IV)

#generate a key for the user 
def key_gen():
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    key = ''.join(random.choice(upper + lower + digits) for _ in range(16))
    return key 

def encrypt(filename, key):
    test = 7
    if len(key) < 16:
        pad = len(key)%16
        pad = 16 - pad
        print("WARNING: The key length must be 16 bytes - padding key with "\
        + str(pad) +" zeros")
        for p in range(pad):
            key += '0'    
    elif len(key) > 16:    
        print('ERROR: Key length must be 16 bytes')
        exit(1)
    
    mode = AES.MODE_CBC
    rand_num = Random.new()
    IV = rand_num.read(16)
    enc_ba = bytearray(IV)

    enc = AES.new(key, mode, IV=IV)
    size = stat(filename).st_size 
    #AES only takes multiple of 16
    padding = size % 16
    file = open(filename, 'rb')
    data = file.read()
    file.close()
    #append EOF character to mark beginning of padding
    if padding == 0:
        data += chr(4)
        for p in range(15):
            data += chr(padding)
    elif padding == 1:
        data += chr(4)
        for p in range(14):
            data += chr(padding)
    else:    
        data += chr(4)
        for p in range(16-(padding+1)):
            data += chr(padding)
        
    #encrypt
    ciphertext = enc.encrypt(data)
    ba = bytearray(ciphertext)
    #prepend IV to encrypted data
    enc_ba.extend(ba)
    return enc_ba

def decrypt(ba, key, outfile, IV=0):    
    mode = AES.MODE_CBC
    
    if len(key) < 16:
        pad = len(key)%16
        pad = 16 - pad
        print("WARNING: The key length must be 16 bytes - padding key with "\
        + str(pad) +" zeros")
        for p in range(pad):
            key += '0'

    if IV == 0:
        IV = parse_IV(ba)
    ciphertext = str(ba)
    #Python3 version
    #ciphertext = bytes(ba)
    dec = AES.new(key, mode, IV=IV)
    plaintext=dec.decrypt(ciphertext)
    #EOF character marks padding
    index = len(plaintext) - plaintext[::-1].find(chr(4)) - 1

    #ignore appeneded padding and prepended IV
    output = plaintext[16:index]
    f = open(outfile, 'w')
    f.write(output)
    f.close()    
