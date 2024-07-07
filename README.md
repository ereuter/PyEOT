# PyEOT
GNU Radio/Python-based decoder for EOT packets

This combination of a GNU Radio Companion flowgraph (EOT.grc) and accompanying pyeot.py will receive
and decode packets from the End-of-Train device.  The GRC flowgraph should be run before running the pyeot script.
Note that pyeot.py MUST be run in Python 3.x.  

ZeroMQ PUB/SUB sockets are used to transfer the bitstream from GRC to the script.  It is set to localhost, but also works 
over an internet connection.  Requires installation of zmq package.

Receive frequnecy should be set 457.9375 MHz.

Note that this software is receive-only, and will not generate packets.  It is intended only for passive monitoring.
This software does not decode packets from the Head-of-Train device.

This is a POC.  No attempt is made to catch or handle errors.  If the GRC flowchart crashes or the TCP connection is interrupted, the receiver script will not know about it, and will not automatically reconnect.  

Also included are slides from my talk at DEFCON 26, and a WAV file with some packets to play with.  

** FILES ADDED 18Jan24 **
- pyeothot.py is an alternative version of pyeot.py that includes HOT decoding
- hot_decoder.py is required to add this function

Not much if any testing has been done with this version.
