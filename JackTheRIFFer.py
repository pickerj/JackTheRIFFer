#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#Authors:           Jacob Mills, James Picker, Kira Lessin
#Date:              10/23/2018
#Description:       A Tool For Audio LSB Steganography Using AES Encryption
#ChangeLog:                   
#                   
#                   

import argparse
import wavparser
import utilities
import os.path

def usage():
    print("Usage:")
    print("./JackTheRIFFER -h")
    print("\tdisplays help information")
    print("./JackTheRIFFER -e <key> -f <file> -w <wave> -o <outfile>")
    print("\tencrypt <file> using AES with <key> and embed in <wave> storing results in <outfile>")
    print("./JackTheRIFFER -d <key> -w <wave> -o <outfile>")
    print("\tdecrypt hidden data in <wave> using AES with <key> and store results in <outfile>\n")

def splash():
    print("""
      _            _    _____ _          ____  ___ _____ _____         
     | | __ _  ___| | _|_   _| |__   ___|  _ \|_ _|  ___|  ___|__ _ __ 
  _  | |/ _` |/ __| |/ / | | | '_ \ / _ \ |_) || || |_  | |_ / _ \ '__|
 | |_| | (_| | (__|   <  | | | | | |  __/  _ < | ||  _| |  _|  __/ |   
  \___/ \__,_|\___|_|\_\ |_| |_| |_|\___|_| \_\___|_|   |_|  \___|_|   
    """)

def validate_args(args):
    if (not args.decrypt and not args.encrypt) or (args.decrypt and args.encrypt) or (not args.outfile) or (not args.wave) or (args.encrypt and not args.file):
        usage()
        exit(1)
    
    if os.path.isfile(args.outfile):
        response = raw_input("WARNING: " \
                "existing file named {} will be overwritten\n\tContinue? (y/n) ".format(args.outfile))
        if (response.lower() not in ["y","yes"]):
            print("Exiting...")
            exit(0)


def main():
    #Use argparse to parse arguments
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('-d','--decrypt',metavar='<key>',help='Uses <key> to decrypt a file')
    parser.add_argument('-e','--encrypt',metavar='<key>',help='Uses <key> to encrypt a file')
    parser.add_argument('-f','--file',metavar='<file>',help='The <file> to encrypt')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-o','--outfile',metavar='<filename>',help='Writes output to <filename>')
    requiredNamed.add_argument('-w','--wave',metavar='<wave>',help='The <wave> hide an encrypted <file> in using LSB steganography')
    args = parser.parse_args()

    # Validates Arguments
    validate_args(args)

    # Print splash
    splash()

    # Load wave
    parsed_wave = wavparser.ParsedWave(args.wave)
    if parsed_wave.binary:
        parsed_wave.debug()
    else:
        print("ERROR: unable to parse {} as a wave".format(args.wave))
        return;

    # Check encrypt/decrypt flag
    if args.encrypt:
        encrypted_data = utilities.encrypt(args.file,args.encrypt)
        parsed_wave.encode_data(encrypted_data)
        parsed_wave.write_to_file(args.outfile)
    else:
        encrypted_data, error_found = parsed_wave.decode_data()
        if error_found:
            print("ERROR: Wave file does not appear to contain encoded data")
            exit(1)
        utilities.decrypt(encrypted_data,args.decrypt,args.outfile)

    print("STATUS: Success! Output file {} has been produced".format(args.outfile))

    # Exit
    exit(0)

if __name__ == '__main__': main()
