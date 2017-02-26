from flask import Flask, render_template, request
from .the_matrix import TheMatrix, DEFAULT_CURRENT_SOURCE_MA
from .layout import Layout

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
    global isReversed
    pixels = [[onOffFrame.getPixel(x, y) for x in range(24)] for y in range(5)]
    return render_template('the_matrix.html', width=24, height=5, current=ledCurrent, pixels=pixels, chip=chip, reversed=isReversed)

@app.route('/reset')
def reset():
    global blinkPWMFrame
    global onOffFrame
    global ledCurrent
    global isReversed

    isReversed = False

    matrix.reset()
    matrix.selectMemoryConfig(1)

    ledCurrent = DEFAULT_CURRENT_SOURCE_MA
    matrix.setCurrentSource(ledCurrent)

    layout = Layout(reversed=isReversed)
    blinkPWMFrame = TheMatrix.BlinkPWMFrame(layout=layout)
    matrix.writeBlinkPWMFrame(0, blinkPWMFrame)

    onOffFrame = TheMatrix.OnOffFrame(layout=layout)
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

@app.route('/setPixel', methods=['POST'])
def setPixel():
    for coords in request.form.getlist('coords[]'):
        x, y = [int(i) for i in coords.split(',')]
        onOffFrame.setPixel(x, y)
    return updateFrame(0)

@app.route('/clearPixel', methods=['POST'])
def clearPixel():
    for coords in request.form.getlist('coords[]'):
        x, y = [int(i) for i in coords.split(',')]
        onOffFrame.setPixel(x, y, 0)
    return updateFrame(0)

@app.route('/setReversed/<reversedFlag>')
def setReversed(reversedFlag):
    global isReversed
    global blinkPWMFrame
    global onOffFrame
    newReversed = reversedFlag == '1'
    if newReversed != isReversed:
        isReversed = newReversed
        newLayout = Layout(reversed=newReversed)
        blinkPWMFrame.layout = newLayout
        onOffFrame.layout = newLayout
        matrix.writeBlinkPWMFrame(0, blinkPWMFrame)
        matrix.writeOnOffFrame(0, onOffFrame)
    return ""

def main():
    reset()
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
