#!/usr/bin/env python

# This assumes you've got two boards configured like this:
#
# +---------------+
# | Address: 0x30 |
# +---------------+
# | Address: 0x37 |
# +---------------+

from __future__ import print_function

from the_matrix import TheMatrix

import getopt, re, sys

def usage():
    print("Usage: %s <banner frames filename>" % (sys.argv[0]), file=sys.stderr)

def frames_from_data(frame_data):
    top = TheMatrix.OnOffFrame()
    bottom = TheMatrix.OnOffFrame()
    for y in range(5):
        for x in range(24):
            if frame_data[y][x] == '#':
                top.setPixel(x, y)
    for y in range(5):
        for x in range(24):
            if frame_data[y+5][x] == '#':
                bottom.setPixel(x, y)
    return (top, bottom)

def display_banner(args):
    top_frames = []
    bottom_frames = []
    for filename in args:
        frame_data = []
        for line in open(filename, 'r'):
            line = line.strip()
            if len(line) == 0:
                top, bottom = frames_from_data(frame_data)
                top_frames.append(top)
                bottom_frames.append(bottom)
                frame_data = []
            else:
                frame_data.append(line)
        if len(frame_data):
            top, bottom = frames_from_data(frame_data)
            top_frames.append(top)
            bottom_frames.append(bottom)

    m1 = TheMatrix(0x30)
    m2 = TheMatrix(0x37)

    m1.reset()
    m2.reset()
    m1.selectMemoryConfig(1)
    m2.selectMemoryConfig(1)
    m1.setClockSync(sync_out=1)
    m2.setClockSync(sync_in=1)
    m1.setCurrentSource(1)
    m2.setCurrentSource(1)

    blinkPWMFrame = TheMatrix.BlinkPWMFrame()
    m1.writeBlinkPWMFrame(0, blinkPWMFrame)
    m2.writeBlinkPWMFrame(0, blinkPWMFrame)

    for frame_num in range(len(top_frames)):
        m1.writeOnOffFrame(frame_num, top_frames[frame_num])
    for frame_num in range(len(bottom_frames)):
        m2.writeOnOffFrame(frame_num, bottom_frames[frame_num])

    m1.setDisplayOptions(loops=7)
    m2.setDisplayOptions(loops=7)
    m1.display(1)
    m2.display(1)
    m1.setMovieMode(frames=len(top_frames))
    m2.setMovieMode(frames=len(bottom_frames))
    m1.setFrameTime(1, enable_scrolling=1)
    m2.setFrameTime(1, enable_scrolling=1)
    m1.displayMovie()
    m2.displayMovie()

def main(args):
    global frames

    try:
        opts, args = getopt.getopt(args, "h")
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()

    display_banner(args)

if __name__ == "__main__":
    main(sys.argv[1:])
