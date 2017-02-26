from __future__ import print_function

from .the_matrix import TheMatrix, DEFAULT_CURRENT_SOURCE_MA
from .detect import detect

import getopt, re, sys

# physical wiring
cs_pairs = [(cathode, anode) for cathode in range(12) for anode in [a for a in range(12) if a != cathode][:10]]

class LEDs(object):

    @classmethod
    def physical_layout(self):
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

    @classmethod
    def logical_layout(self):
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

    @classmethod
    def display_leds(self, leds):
        """Display listed LEDs (logical number in hex or x,y coordinates in decimal)"""
        for m in matrix:
            m.reset()
            m.selectMemoryConfig(1)
            m.setCurrentSource(DEFAULT_CURRENT_SOURCE_MA)

            blinkPWMFrame = TheMatrix.BlinkPWMFrame()
            m.writeBlinkPWMFrame(0, blinkPWMFrame)

            onOffFrame = TheMatrix.OnOffFrame()
            for led in leds:
                x,y = 0,0
                coords = led.split(',')
                if len(coords) == 2:
                    x, y = [int(n) for n in coords]
                else:
                    match = re.match('^(/?)cs(\d+)$', led, re.IGNORECASE)
                    if match:
                        low = match.group(1)
                        signal = int(match.group(2))
                        connected_pairs = [i for i in range(len(cs_pairs)) if cs_pairs[i][0 if low else 1] == signal]
                        for pair_index in connected_pairs:
                            x = int(pair_index/5)
                            y = pair_index % 5
                            leds += ["%d,%d" % (x, y)]
                        continue
                    else:
                        led = int(led, 16)
                        hi = int(led/16)
                        lo = led % 16
                        x = hi*2 + int(lo/5)
                        y = lo % 5
                assert(x in range(24))
                assert(y in range(5))
                onOffFrame.setPixel(x, y)
            m.writeOnOffFrame(0, onOffFrame)

            m.setDisplayOptions()
            m.display(1)

            m.displayPictureFrame(0)

def usage():
    print("Usage: {} [-a <address>[,<address>...]] [-h] [-l] [-p] <led_numbers>".format(sys.argv[0]), file=sys.stderr)

def main(args):
    global matrix

    addresses = []

    try:
        opts, args = getopt.getopt(args, "hlpa:")
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
            LEDs.logical_layout()
        elif opt == '-p':
            LEDs.physical_layout()
        elif opt == '-a':
            addresses = [int(address, 16) for address in arg.split(',')]

    if len(opts)>0 and len(args)==0:
        sys.exit(0)

    if len(addresses) == 0:
        addresses = detect()

    matrix = [TheMatrix(address) for address in addresses]

    LEDs.display_leds(args)

def command_line():
    main(sys.argv[1:])

if __name__ == "__main__":
    command_line(sys.argv[1:])
