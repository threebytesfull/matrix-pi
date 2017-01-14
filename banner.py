#!/usr/bin/env python

from __future__ import print_function

from the_matrix import TheMatrix

import getopt, re, sys

def usage():
    print("Usage: %s <banner frames filename>" % (sys.argv[0]), file=sys.stderr)

def frame_from_data(frame_data):
    f = TheMatrix.OnOffFrame()
    for y in range(5):
        for x in range(24):
            if frame_data[y][x] == '#':
                f.setPixel(x, y)
    return f

def display_banner(args):
    frames = []
    for filename in args:
        frame_data = []
        for line in open(filename, 'r'):
            line = line.strip()
            if len(line) == 0:
                frames.append(frame_from_data(frame_data))
                frame_data = []
            else:
                frame_data.append(line)
        if len(frame_data):
            frames.append(frame_from_data(frame_data))

    assert len(frames) <= 36, "cannot store more than 36 frames"

    m = TheMatrix()
    m.reset()
    m.selectMemoryConfig(1)
    m.setClockSync()
    m.setCurrentSource(1)
    blinkPWMFrame = TheMatrix.BlinkPWMFrame()
    m.writeBlinkPWMFrame(0, blinkPWMFrame)
    for frame_num in range(len(frames)):
        m.writeOnOffFrame(frame_num, frames[frame_num])
    m.setDisplayOptions(loops=7)
    m.display(1)
    m.setMovieMode(frames=len(frames))
    m.setFrameTime(1, enable_scrolling=1)
    m.displayMovie()

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

    if len(args) < 1:
        usage()
        sys.exit(2)

    display_banner(args)

if __name__ == "__main__":
    main(sys.argv[1:])
