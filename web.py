#!/usr/bin/env python

from flask import Flask, render_template
from the_matrix import TheMatrix

import re

app = Flask(__name__)

matrix = TheMatrix()

cs_pairs = [(anode, cathode) for cathode in range(12) for anode in [a for a in range(12) if a != cathode][:10]]
chip = [{'label': label} for label in 'GND CS6 VDD CS7 CS8 CS9 GND CS11 CS10 VDD IRQ SYNC RSTN GND SCL SDA ADDR VDD VDD CS5 CS4 GND CS2 CS3 CS0 VDD CS1 GND'.split()]
for pin in chip:
    match = re.match('^CS(\d+)', pin['label'])
    if match:
        signal = int(match.group(1))
        pin['clickable'] = True
        # get anode-connected LEDs
        anode_led_indices = [i for i in range(len(cs_pairs)) if cs_pairs[i][0] == signal]
        pin['anode_leds'] = [[int(i/5), i%5] for i in anode_led_indices]
        # get cathode-connected LEDs
        cathode_led_indices = [i for i in range(len(cs_pairs)) if cs_pairs[i][1] == signal]
        pin['cathode_leds'] = [[int(i/5), i%5] for i in cathode_led_indices]

def updateFrame(frameNumber):
    matrix.writeOnOffFrame(frameNumber, onOffFrame)
    return ""

@app.route('/')
def main_route():
    global ledCurrent
    global onOffFrame
    pixels = [[onOffFrame.getPixel(x, y) for x in range(24)] for y in range(5)]
    return render_template('the_matrix.html', width=24, height=5, current=ledCurrent, pixels=pixels, chip=chip)

@app.route('/reset')
def reset():
    global blinkPWMFrame
    global onOffFrame
    global ledCurrent

    matrix.reset()
    matrix.selectMemoryConfig(1)

    ledCurrent = 1
    matrix.setCurrentSource(ledCurrent)

    blinkPWMFrame = TheMatrix.BlinkPWMFrame()
    matrix.writeBlinkPWMFrame(0, blinkPWMFrame)

    onOffFrame = TheMatrix.OnOffFrame()
    matrix.writeOnOffFrame(0, onOffFrame)

    matrix.setDisplayOptions()
    matrix.display(1)
    matrix.displayPictureFrame(0)
    return ""

@app.route('/setCurrent/<current>')
def setCurrent(current):
    global ledCurrent
    ledCurrent = int(current)
    matrix.setCurrentSource(ledCurrent)
    return ""

@app.route('/allOff')
def allOff():
    global blinkPWMFrame
    global onOffFrame

    blinkPWMFrame = TheMatrix.BlinkPWMFrame()
    matrix.writeBlinkPWMFrame(0, blinkPWMFrame)

    onOffFrame = TheMatrix.OnOffFrame(0)
    matrix.writeOnOffFrame(0, onOffFrame)
    return ""

@app.route('/allOn')
def allOn():
    global blinkPWMFrame
    global onOffFrame

    blinkPWMFrame = TheMatrix.BlinkPWMFrame()
    matrix.writeBlinkPWMFrame(0, blinkPWMFrame)

    onOffFrame = TheMatrix.OnOffFrame(1)
    matrix.writeOnOffFrame(0, onOffFrame)
    return ""

@app.route('/setPixel/<x>/<y>')
def setPixel(x, y):
    x, y = int(x), int(y)
    onOffFrame.setPixel(x, y)
    return updateFrame(0)

@app.route('/clearPixel/<x>/<y>')
def clearPixel(x, y):
    x, y = int(x), int(y)
    onOffFrame.setPixel(x, y, 0)
    return updateFrame(0)

if __name__ == "__main__":
    reset()
    app.run(host='0.0.0.0')
