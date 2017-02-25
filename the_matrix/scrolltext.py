from __future__ import print_function

from .the_matrix import TheMatrix
from .pixel_font import *

import getopt, math, re, sys

DEFAULT_ADDRESS = 0x30

class ScrollText(object):
    """Class to provide scrolling text for The Matrix"""

    @classmethod
    def display_banner(self, args):
        frames = [TheMatrix.OnOffFrame() for _ in range(len(matrix))]
        font = PixelFont5Narrow()
        pixel_data = font.string(' '.join(args))

        # check message length, allowing for one extra blank frame
        num_frames = int(math.ceil(len(pixel_data[0]) / 24.0))
        assert num_frames < 36, 'message too long to fit in 36 frames'

        if len(pixel_data[0]) % 24 != 0:
            for y in range(5):
                pixel_data[y] += '.' * (24 - (len(pixel_data[y]) % 24))

        for i in range(num_frames):
            frame = TheMatrix.OnOffFrame()
            for y in range(5):
                pixel_row = pixel_data[y][24*i:24*i+24]
                for x in range(24):
                    if pixel_row[x] == '#':
                        frame.setPixel(x, y)
            frames.append(frame)

        # turn displays off first to avoid losing sync
        for i in range(len(matrix)):
            matrix[i].display(0)

        for i in range(len(matrix)):
            m = matrix[i]
            m.reset()
            m.selectMemoryConfig(1)
            m.setClockSync(sync_out=1 if i==0 else 0, sync_in=0 if i==0 else 1)
            m.setCurrentSource(1)
            blinkPWMFrame = TheMatrix.BlinkPWMFrame()
            m.writeBlinkPWMFrame(0, blinkPWMFrame)
            for frame_num in range(len(frames)):
                m.writeOnOffFrame(frame_num, frames[frame_num])
            for frame_num in range(min(len(matrix), 36-len(frames))):
                m.writeOnOffFrame(frame_num + len(frames), TheMatrix.OnOffFrame())
            m.setDisplayOptions(loops=7)
            m.setMovieMode(frames=len(frames))
            m.setFrameTime(1, enable_scrolling=1)

        for i in range(len(matrix)):
            m = matrix[i]
            m.display(1)
            m.displayMovie(frame=i)

def usage():
    print("Usage: {} [-a <address>[,<address>...]] <text>".format(sys.argv[0]), file=sys.stderr)

def main(args):
    global matrix

    addresses = [DEFAULT_ADDRESS]

    try:
        opts, args = getopt.getopt(args, 'ha:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        if opt == '-a':
            addresses = [int(address, 16) for address in arg.split(',')]

    if len(args) < 1:
        usage()
        sys.exit(2)

    matrix = [TheMatrix(address) for address in addresses]

    ScrollText.display_banner(args)

def command_line():
    main(sys.argv[1:])
