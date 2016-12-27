# Test script for Boldport TheMatrix

Here's a quick Python test script to drive your board from a Raspberry Pi.

## Connections

To connect to the I2C bus on the Raspberry Pi, connect directly to the
expansion header. Here's a top-down view - pin 1 is closest to the display
connector:

        VCC  1  2
        SDA  3  4
        SCL  5  6
             7  8
        GND  9 10
            11 12
            13 14
            15 16
            17 18
            19 20
            21 22
            23 24
            25 26
            27 28
            29 30
            31 32
            33 34
            35 36
            37 38
            39 40
        [USB ports this end]

## Usage

From your Raspberry Pi shell, run `i2cdetect` to check that your TheMatrix is
responding and has the address you're expecting:

    i2cdetect -y 1

By default, TheMatrix will have address 0x30 if you haven't added a resistor at
R4 to specify otherwise.

If your address matches the default, you can just run the Python script
directly:

    python the_matrix.py

and that should light up all the LEDs. There's some extra functionality in
there (it can set/clear individual pixels, handle PWM and blink frames, etc)
but it's not complete or tested yet.

If your board has a different address, you'll want to change the address
hard-coded at the top of the script.