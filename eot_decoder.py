#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyEOT End-of-Train Device Decoder
Copyright (c) 2018 Eric Reuter

This source file is subject of the GNU general public license.

history:    2018-08-09 Initial Version

purpose:    Class to parse EOT packet and generate BCH checkbits
            for verification.

            Requires helpers.py
"""

import helpers


class EOT_decode():
    def __init__(self, buffer):
        self.packet = buffer[0:74]
        self.frame_sync = self.packet[0:11]
        self.data_block = self.packet[11:56]
        self.batt_cond = (self.packet[13:15][::-1])
        self.message_type = self.packet[15:18]
        self.unit_addr = int((self.packet[18:35][::-1]), 2)
        self.pressure = int((self.packet[35:42][::-1]), 2)
        self.batt_charge = \
            ("{}%".format(int(int((self.packet[42:49][::-1]), 2) / 127 * 100)))
        self.spare = self.packet[49]
        self.valve_ckt_stat = self.packet[50]
        self.conf_ind = self.packet[51]
        self.turbine = self.packet[52]
        self.motion = self.packet[53]
        self.mkr_batt = self.packet[54]
        self.mkr_light = self.packet[55]
        self.checkbitsRx = self.packet[56:74]

        self.batt_cond_dict = {"11": "OK",
                               "10": "Low",
                               "01": "Very Low",
                               "00": "Not Monitored"}
        self.batt_cond_text = self.batt_cond_dict[self.batt_cond]

        if (self.message_type == "111"):
            if (self.conf_ind == "0"):
                self.arm_status = "Arming"
            else:
                self.arm_status = "Armed"
        else:
            self.arm_status = "Normal"

        self.generator = '1111001101000001111'  # BCH generator polynomial
        self.cipher_key = '101011011101110000'  # XOR cipher key
        self.data_block = helpers.reverse(self.data_block)
        self.checkbits = helpers.checkbits(self.data_block, self.generator)
        self.checkbits_cipher = helpers.xor(self.checkbits, self.cipher_key)
        self.valid = (self.checkbits_cipher == self.checkbitsRx)  # a match?

    def get_packet(self):
        return ''.join(self.packet)
