#!/usr/bin/python

import sys, os

# Add path to pyRadioHeadiRF95 module
sys.path.append(os.path.dirname(__file__) + "/../")

import pyRadioHeadRF95 as radio
import time

rf95 = radio.RF95()

rf95.init()

rf95.setTxPower(14, False)
rf95.setFrequency(915)

rf95.setSignalBandwidth(rf95.Bandwidth500KHZ)
rf95.setSpreadingFactor(rf95.SpreadingFactor8)
rf95.setCodingRate4(rf95.CodingRate4_6)

print "StartUp Done!"
print "Receiving..."


while True:
    if rf95.available():
        print "Available"
        (msg, l) = rf95.recv()
        print "Received: " + msg + " (" + str(l) + ")"
        time.sleep(0.1)
    else:
        time.sleep(0.05)
