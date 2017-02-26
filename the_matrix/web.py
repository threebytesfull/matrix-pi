from flask import Flask, render_template, request
from .the_matrix import TheMatrix, DEFAULT_CURRENT_SOURCE_MA
from .layout import Layout
from .detect import detect

import re

app = Flask(__name__)

addresses = detect()
matrices = dict((address, TheMatrix(address)) for address in addresses)

blinkPWMFrames = dict((address, None) for address in addresses)
onOffFrames = dict((address, None) for address in addresses)
isReversed = dict((address, False) for address in addresses)
ledCurrents = dict((address, DEFAULT_CURRENT_SOURCE_MA) for address in addresses)
resetCurrents = dict((address, DEFAULT_CURRENT_SOURCE_MA) for address in addresses)

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

def updateFrame(address, frameNumber):
    matrices[address].writeOnOffFrame(frameNumber, onOffFrames[address])
    return ""

@app.route('/')
def main_route():
    pixels = dict((address, [[onOffFrames[address].getPixel(x, y) for x in range(24)] for y in range(5)]) for address in matrices.keys())
    return render_template(
        'the_matrix.html',
        width=24,
        height=5,
        current=ledCurrents,
        resetCurrents=resetCurrents,
        pixels=pixels,
        chip=chip,
        reversed=isReversed,
        addresses=sorted(matrices.keys())
    )

@app.route('/reset', methods=['POST'])
def reset():
    try:
        addresses = [int(request.form['address'])]
    except:
        addresses = matrices.keys()

    for address in addresses:
        isReversed[address] = False
        matrix = matrices[address]

        matrix.reset()
        matrix.selectMemoryConfig(1)

        ledCurrents[address] = DEFAULT_CURRENT_SOURCE_MA
        matrix.setCurrentSource(ledCurrents[address])

        layout = Layout(reversed=isReversed[address])
        blinkPWMFrames[address] = TheMatrix.BlinkPWMFrame(layout=layout)
        matrix.writeBlinkPWMFrame(0, blinkPWMFrames[address])

        onOffFrames[address] = TheMatrix.OnOffFrame(layout=layout)
        matrix.writeOnOffFrame(0, onOffFrames[address])

        matrix.setDisplayOptions()
        matrix.display(1)
        matrix.displayPictureFrame(0)

    return ""

@app.route('/setCurrent', methods=['POST'])
def setCurrent():
    address = int(request.form['address'])
    current = int(request.form['current'])

    ledCurrents[address] = current

    matrices[address].setCurrentSource(ledCurrents[address])

    return ""

@app.route('/allOff', methods=['POST'])
def allOff():
    address = int(request.form['address'])

    blinkPWMFrames[address] = TheMatrix.BlinkPWMFrame()
    onOffFrames[address] = TheMatrix.OnOffFrame(0)

    matrix = matrices[address]
    matrix.writeBlinkPWMFrame(0, blinkPWMFrames[address])
    matrix.writeOnOffFrame(0, onOffFrames[address])

    return ""

@app.route('/allOn', methods=['POST'])
def allOn():
    address = int(request.form['address'])

    blinkPWMFrames[address] = TheMatrix.BlinkPWMFrame()
    onOffFrames[address] = TheMatrix.OnOffFrame(1)

    matrix = matrices[address]
    matrix.writeBlinkPWMFrame(0, blinkPWMFrames[address])
    matrix.writeOnOffFrame(0, onOffFrames[address])

    return ""

@app.route('/setPixel', methods=['POST'])
def setPixel():
    address = int(request.form['address'])

    for coords in request.form.getlist('coords[]'):
        x, y = [int(i) for i in coords.split(',')]
        onOffFrames[address].setPixel(x, y)

    return updateFrame(address, 0)

@app.route('/clearPixel', methods=['POST'])
def clearPixel():
    address = int(request.form['address'])

    for coords in request.form.getlist('coords[]'):
        x, y = [int(i) for i in coords.split(',')]
        onOffFrames[address].setPixel(x, y, 0)

    return updateFrame(address, 0)

@app.route('/setReversed', methods=['POST'])
def setReversed():
    address = int(request.form['address'])
    reversedFlag = request.form['reversed']

    newReversed = reversedFlag == 'true'
    if newReversed != isReversed[address]:
        isReversed[address] = newReversed
        newLayout = Layout(reversed=newReversed)
        blinkPWMFrames[address].layout = newLayout
        onOffFrames[address].layout = newLayout

        matrix = matrices[address]
        matrix.writeBlinkPWMFrame(0, blinkPWMFrames[address])
        matrix.writeOnOffFrame(0, onOffFrames[address])

    return ""

def main():
    reset()
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
