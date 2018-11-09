#!/usr/bin/python

def twos_comp(num,bit_length):
    if num < 0:
        num = (1 << bit_length) + num
    else:
        if (num & (1 << (bit_length - 1))) != 0:
            num = num - (1 << bit_length)
    return num
