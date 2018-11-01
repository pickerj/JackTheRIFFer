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

def usage():
    print("Usage:")
    print("./JackTheRIFFER -h")
    print("\tdisplays help information")
    print("./JackTheRIFFER -e <key> -f <file> -w <wave>")
    print("\tencrypt <file> using AES with <key> and embed in <wave>")
    print("./JackTheRIFFER -d <key> -f <file> -w <wave>")
    print("\tdecrypt hidden data in <wave> using AES with <key> and store results in <file>")

def validate_args(args):
    if (not args.decrypt and not args.encrypt) or (args.decrypt and args.encrypt):
        usage()
        exit(1)
    if (args.decrypt):
        # TODO: Check to see if args.file exists before displaying warning
        response = raw_input("WARNING: if decryption is successful, " \
                "existing files named {} will be overwritten\n\tContinue? (y/n) ".format(args.file))
        if (response.lower() not in ["y","yes"]):
            print("Exiting...")
            exit(0)

def main():
    #Use argparse to parse arguments
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('-d','--decrypt',metavar='<key>',help='Uses <key> to decrypt a file')
    parser.add_argument('-e','--encrypt',metavar='<key>',help='Uses <key> to encrypt a file')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-f','--file',metavar='<file>',help='The <file> to encrypt or produce after decryption',required=True)
    requiredNamed.add_argument('-w','--wave',metavar='<wave>',help='The <wave> hide an encrypted <file> in using LSB steganography',required=True)
    args = parser.parse_args()

    # Validates Arguments
    validate_args(args)


    # Exit
    exit(0)

if __name__ == '__main__': main()
