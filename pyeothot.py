#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyEOT End-of-Train Device Decoder
Copyright (c) 2018 Eric Reuter

This source file is subject of the GNU general public license.

history:    2018-08-09 Initial Version

purpose:    Receives demodulated FFSK bitstream from GNU Radio, indentifes
            potential packets, and passes them to decoder classes for
            parsing and verification.  Finally human-readable data are printed
            to stdout.

            Requires eot_decoder.py and helpers.py
"""

import datetime
import collections
from eot_decoder import EOT_decode
from hot_decoder import HOT_decode
import zmq

# Socket to talk to server
context = zmq.Context()
sock = context.socket(zmq.SUB)

# create fixed length queue
queue = collections.deque(maxlen=256)


def printEOT(EOT):
    localtime = str(datetime.datetime.now().
                    strftime('%Y-%m-%d %H:%M:%S.%f'))[:-3]
    print("")
    print("EOT {}".format(localtime))
    #   print(EOT.get_packet())
    print("---------------------")
    print("Unit Address:   {}".format(EOT.unit_addr))
    print("Pressure:       {} psig".format(EOT.pressure))
    print("Motion:         {}".format((EOT.motion)))
    print("Marker Light:   {}".format((EOT.mkr_light)))
    print("Turbine:        {}".format((EOT.turbine)))
    print("Battery Cond:   {}".format(EOT.batt_cond_text))
    print("Battery Charge: {}".format(EOT.batt_charge))
    print("Arm Status:     {}".format(EOT.arm_status))


def printHOT(HOT):
    localtime = str(datetime.datetime.now().
                    strftime('%Y-%m-%d %H:%M:%S.%f'))[:-3]
    print("")
    print("HOT {}".format(localtime))
    print("-------------------")
    print("Unit Address: {}".format(HOT.unit_addr))
    print("Command:      {}".format(HOT.command_text))


def main():
    #  Connect to GNU Radio and subscribe to stream
    sock.connect("tcp://localhost:5555")
    sock.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        newData = sock.recv()  # get whatever data are available
        for byte in newData:
            queue.append(str(byte))  # append each new symbol to deque

            buffer = ''  # clear buffer
            for bit in queue:  # move deque contents into buffer
                buffer += bit

            if (buffer.find('10101011100010010') == 0):  # look for frame sync
                EOT = EOT_decode(buffer[6:])  # first 6 bits are bit sync
                if (EOT.valid):
                    printEOT(EOT)

            if (buffer.find('010101100011110001000100101001') == 0):
                HOT = HOT_decode(buffer[6:])
                if (HOT.valid):
                    printHOT(HOT)


main()
