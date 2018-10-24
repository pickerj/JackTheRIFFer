#!/usr/bin/python2.7
#Authors:           Jacob Mills, James Picker, Kira Lessin
#Date:              10/23/2018
#Description:       A Tool For Audio LSB Steganography Using AES Encryption
#ChangeLog:                   
#                   
#                   
#

import argparse
import wavparser

def main():
    #Use argparse to parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',metavar='<key>',help='Uses <key> to decrypt a file')
    parser.add_argument('-e',metavar='<key>',help='Uses <key> to encrypt a file')
    parser.add_argument('-f',metavar='<file>',help='The <file> to encrypt or produce after decryption')
    parser.add_argument('-w',metavar='<wave>',help='The <wave> hide an encrypted <file> in using LSB steganography')
    args = parser.parse_args()

    # Validates Arguments
    exit(0)

if __name__ == '__main__': main()
