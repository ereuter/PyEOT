#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyEOT End-of-Train Device Decoder
Copyright (c) 2018 Eric Reuter

This source file is subject of the GNU general public license.

history:    2018-08-09 Initial Version

purpose:    Misc. functions used by eot_decoder.py

            Function XOR() and mod2div() adapted from:
            https://www.geeksforgeeks.org/cyclic-redundancy-check-python/
"""


# XOR two strings of bytes representing binary symbols
def xor(a, b):
    result = []
    for i in range(len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


# Reverse string
def reverse(data):
    return ''.join(data[::-1])


# Perform modulo-2 division on two strings of binary symbols
def mod2div(dividend, divisor):

    # Number of bits to be XORed at a time.
    pick = len(divisor)

    # Slicing the dividend to appropriate
    # length for particular step
    tmp = dividend[0:pick]

    while pick < len(dividend):

        if tmp[0] == '1':

            # replace the dividend by the result
            # of XOR and pull 1 bit down
            tmp = xor(divisor[1:], tmp[1:]) + dividend[pick]

        else:   # If leftmost bit is '0'
            # If the leftmost bit of the dividend (or the
            # part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an
            # all-0s divisor.
            tmp = xor(('0'*pick)[1:], tmp[1:]) + dividend[pick]

        # increment pick to move further
        pick += 1

    # For the last n bits, we have to carry it out
    # normally as increased value of pick will cause
    # Index Out of Bounds.
    if tmp[0] == '1':
        tmp = xor(divisor[1:], tmp[1:])
    else:
        tmp = xor(('0'*pick)[1:], tmp[1:])

    remainder = tmp
    return remainder


# Calculate BCH checkbits
def checkbits(data, key):
    appended_data = data + '0'*(len(key)-1)  # Appends n-1 zeros at end of data
    remainder = mod2div(appended_data, key)
    return ''.join(remainder)
