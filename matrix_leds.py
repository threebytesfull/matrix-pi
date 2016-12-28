#!/usr/bin/env python

from __future__ import print_function

from the_matrix import TheMatrix

import sys, getopt

# physical wiring
cs_pairs = [(cathode, anode) for cathode in range(12) for anode in [a for a in range(12) if a != cathode][:10]]

def usage():
    print("Usage: %s [-h] [-l] [-p] <led_numbers>" % sys.argv[0], file=sys.stderr)

def physical_layout():
    print("Physical layout:")
    print(("+" + "-"*11)*12 + "+")
    print("|"+("|".join([("/CS%d" % segment).center(11) for segment in range(12)])+"|"))
    print(("+" + "-"*5)*24 + "+")
    for y in range(5):
        line = ""
        for segment in range(12):
            segment_pairs = cs_pairs[segment*10:segment*10+10]
            line += "|" + ("CS%d" % segment_pairs[y][1]).center(5)
            line += "|" + ("CS%d" % segment_pairs[y+5][1]).center(5)
        print("%s|" % line)
        print(("+" + "-"*5)*24 + "+")
    print("")

def logical_layout():
    print("Logical layout:")
    print(("+" + "-"*11)*12 + "+")
    print("|"+("|".join([("Segment %X" % segment).center(11) for segment in range(12)])+"|"))
    print(("+" + "-"*5)*24 + "+")
    for y in range(5):
        line = ""
        for segment in range(12):
            first_segment_led = 16*segment + y
            line += "|" + ("%02X" % first_segment_led).center(5)
            line += "|" + ("%02X" % (first_segment_led + 5)).center(5)
        print("%s|" % line)
        print(("+" + "-"*5)*24 + "+")
    print("")

def display_leds(leds):
    """Display listed LEDs (logical number in hex or x,y coordinates in decimal)"""
    matrix = TheMatrix()

    matrix.reset()
    matrix.selectMemoryConfig(1)
    matrix.setCurrentSource(1)

    blinkPWMFrame = TheMatrix.BlinkPWMFrame()
    matrix.writeBlinkPWMFrame(0, blinkPWMFrame)

    onOffFrame = TheMatrix.OnOffFrame()
    for led in leds:
        x,y = 0,0
        coords = led.split(',')
        if len(coords) == 2:
            x, y = [int(n) for n in coords]
        else:
            led = int(led, 16)
            hi = int(led/16)
            lo = led % 16
            x = hi*2 + int(lo/5)
            y = lo % 5
        assert(x in range(24))
        assert(y in range(5))
        onOffFrame.setPixel(x, y)
    matrix.writeOnOffFrame(0, onOffFrame)

    matrix.setDisplayOptions()
    matrix.display(1)

    matrix.displayPictureFrame(0)

def main(args):
    try:
        opts, args = getopt.getopt(args, "hlp")
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args+opts) == 0:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-l':
            logical_layout()
        elif opt == '-p':
            physical_layout()

    display_leds(args)

if __name__ == "__main__":
    main(sys.argv[1:])
