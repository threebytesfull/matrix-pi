#!/usr/bin/env python

from the_matrix import TheMatrix

def zigzag_frame(offset=0):
    y = 0
    inc = 1
    frame = TheMatrix.OnOffFrame()
    for x in range(24):
        frame.setPixel((x+offset) % 24, y, 1)
        if (y + inc not in range(5)):
            inc = -inc
        y += inc
    return frame

matrix = TheMatrix()

matrix.reset()
matrix.selectMemoryConfig(1)
matrix.setCurrentSource(1)

blinkPWMFrame = TheMatrix.BlinkPWMFrame()
matrix.writeBlinkPWMFrame(0, blinkPWMFrame)

for frame_num in range(8):
    matrix.writeOnOffFrame(frame_num, zigzag_frame(8-frame_num))

matrix.setDisplayOptions(loops=7)
matrix.display(1)

matrix.setMovieMode(frames=8)
matrix.setFrameTime(1)
matrix.displayMovie()
