from __future__ import print_function

from .the_matrix import TheMatrix, DEFAULT_CURRENT_SOURCE_MA
from .pixel_font import *
from .detect import detect

import getopt, sys

def usage():
    print("Usage: {} [-a <address>[,<address>...]] [-b <bus_number>]".format(sys.argv[0]), file=sys.stderr)

def main(args):
    addresses = []
    bus_number = 1

    try:
        opts, args = getopt.getopt(args, 'ha:b:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        if opt == '-a':
            addresses = [int(address, 16) for address in arg.split(',')]
        if opt == '-b':
            bus_number = int(arg)

    if len(addresses) == 0:
        addresses = detect(bus_number)

    font = PixelFont5Narrow()

    for address in addresses:
        matrix = TheMatrix(address, bus_number=bus_number)
        pixel_data = font.string('0x%02x' % address)
        if len(pixel_data[0]) % 24 != 0:
            for y in range(5):
                pixel_data[y] += '.' * (24 - (len(pixel_data[y]) % 24))

        frame = TheMatrix.OnOffFrame()
        for y in range(5):
            pixel_row = pixel_data[y][0:24]
            for x in range(24):
                if pixel_row[x] == '#':
                    frame.setPixel(x, y)

        matrix.display(0)
        matrix.reset()
        matrix.selectMemoryConfig(1)
        matrix.setCurrentSource(DEFAULT_CURRENT_SOURCE_MA)
        blinkPWMFrame = TheMatrix.BlinkPWMFrame()
        matrix.writeBlinkPWMFrame(0, blinkPWMFrame)
        matrix.writeOnOffFrame(0, frame)
        matrix.setDisplayOptions(loops=0)
        matrix.display(1)
        matrix.displayPictureFrame()

def command_line():
    main(sys.argv[1:])
