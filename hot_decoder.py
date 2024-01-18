#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 20:16:56 2017

@author: ereuter
"""
import helpers

"""
This class decodes and verifies an HOT packet.

"""


class HOT_decode():

    def __init__(self, buffer):  # 01010101 = status req, 10101010 = emergency

        self.packet = buffer[0:216]
        self.frame_sync = self.packet[0:24]
        self.data_block = self.packet[24:54]
        self.unit_addr = int((self.packet[29:46][::-1]), 2)
        self.command = self.packet[46:54][::-1]
        self.checkbitsRx = self.packet[54:87]
        self.parity = self.packet[87]

        self.command_text = "EMERGENCY" if (self.command == '10101010') else "Status Request"

        # BCH generator polynomial
        self.generator = '1110011011010111000010110011111011'
        self.data_block = helpers.reverse(self.data_block)
        self.checkbits = helpers.checkbits(self.data_block, self.generator)

        self.parity_check = str(self.packet[24:87].count('1') % 2) == self.parity

        self.valid = ((self.checkbits == self.checkbitsRx) & self.parity_check)
        self.valid = (self.checkbits == self.checkbitsRx)  #ignore parity for testing

    def get_packet(self):
        return ''.join(self.packet)
