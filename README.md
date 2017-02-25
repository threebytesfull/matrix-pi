# Driver Module for Boldport TheMatrix

Here's a Python module to drive your board from a Raspberry Pi.

## Prerequisites

You need I2C set up on your Raspberry Pi. If you haven't done this before, you
need to enable the I2C hardware:

    sudo raspi-config

Choose `9 Advanced Options`, `A6 I2C`, `Yes`, `Ok`, `Finish`.

Next, you'll need to install the I2C support for Python:

    sudo apt-get install python-smbus python3-smbus

It's possible that you'll need to reboot at this point, but I've not found that
necessary on the Raspberry Pi boards I've tried so far.

## Installation

The module is available as a Python package, so you can install it with `pip`.

    # Install for Python 2
    pip install the_matrix

or

    # Install for Python 3
    pip3 install the_matrix

Depending on your system configuration, you may need to run those with
superuser privileges:

    # Superuser install for Python 2
    sudo pip install the_matrix

or

    # Superuser install for Python 3
    sudo pip3 install the_matrix

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
R4 to specify otherwise. The output should look something like this:

         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: 30 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --

## [the_matrix_leds](./the_matrix/leds.py)

There's a script called `the_matrix_leds` which can set specified LEDs on
individually - that may be useful for testing too. You can specify LEDs either
by coordinates or by their logical number in hex, or groups of LEDs by AS1130
pin:

    # turn on three LEDs
    the_matrix_leds 7 9 b0

    # turn on top left corner and top right corner LEDs
    the_matrix_leds 0,0 23,0

    # turn on all LEDs whose anode connects to CS2
    the_matrix_leds cs2

    # turn on all LEDs whose cathode connects to CS10
    the_matrix_leds /CS10

If the board you are testing is not at the default address of 0x30, you can
specify an address on the command line with `-a`:

    # turn on three LEDs, board address 0x37
    the_matrix_leds -a 0x37 7 9 b0

It can also show a map of the physical connections for each LED:

    the_matrix_leds -p

    Physical layout:
    +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    |    /CS0   |    /CS1   |    /CS2   |    /CS3   |    /CS4   |    /CS5   |    /CS6   |    /CS7   |    /CS8   |    /CS9   |   /CS10   |   /CS11   |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | CS1 | CS6 | CS0 | CS6 | CS0 | CS6 | CS0 | CS6 | CS0 | CS6 | CS0 | CS6 | CS0 | CS5 | CS0 | CS5 | CS0 | CS5 | CS0 | CS5 | CS0 | CS5 | CS0 | CS5 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | CS2 | CS7 | CS2 | CS7 | CS1 | CS7 | CS1 | CS7 | CS1 | CS7 | CS1 | CS7 | CS1 | CS7 | CS1 | CS6 | CS1 | CS6 | CS1 | CS6 | CS1 | CS6 | CS1 | CS6 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | CS3 | CS8 | CS3 | CS8 | CS3 | CS8 | CS2 | CS8 | CS2 | CS8 | CS2 | CS8 | CS2 | CS8 | CS2 | CS8 | CS2 | CS7 | CS2 | CS7 | CS2 | CS7 | CS2 | CS7 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | CS4 | CS9 | CS4 | CS9 | CS4 | CS9 | CS4 | CS9 | CS3 | CS9 | CS3 | CS9 | CS3 | CS9 | CS3 | CS9 | CS3 | CS9 | CS3 | CS8 | CS3 | CS8 | CS3 | CS8 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    | CS5 | CS10| CS5 | CS10| CS5 | CS10| CS5 | CS10| CS5 | CS10| CS4 | CS10| CS4 | CS10| CS4 | CS10| CS4 | CS10| CS4 | CS10| CS4 | CS9 | CS4 | CS9 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

and a logical map with the LED numbers in hex (the same numbers it expects on
the command line):

    the_matrix_leds -l

    Logical layout:
    +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Segment 0 | Segment 1 | Segment 2 | Segment 3 | Segment 4 | Segment 5 | Segment 6 | Segment 7 | Segment 8 | Segment 9 | Segment A | Segment B |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  00 |  05 |  10 |  15 |  20 |  25 |  30 |  35 |  40 |  45 |  50 |  55 |  60 |  65 |  70 |  75 |  80 |  85 |  90 |  95 |  A0 |  A5 |  B0 |  B5 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  01 |  06 |  11 |  16 |  21 |  26 |  31 |  36 |  41 |  46 |  51 |  56 |  61 |  66 |  71 |  76 |  81 |  86 |  91 |  96 |  A1 |  A6 |  B1 |  B6 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  02 |  07 |  12 |  17 |  22 |  27 |  32 |  37 |  42 |  47 |  52 |  57 |  62 |  67 |  72 |  77 |  82 |  87 |  92 |  97 |  A2 |  A7 |  B2 |  B7 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  03 |  08 |  13 |  18 |  23 |  28 |  33 |  38 |  43 |  48 |  53 |  58 |  63 |  68 |  73 |  78 |  83 |  88 |  93 |  98 |  A3 |  A8 |  B3 |  B8 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
    |  04 |  09 |  14 |  19 |  24 |  29 |  34 |  39 |  44 |  49 |  54 |  59 |  64 |  69 |  74 |  79 |  84 |  89 |  94 |  99 |  A4 |  A9 |  B4 |  B9 |
    +-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

## [the_matrix_scrolltext](./the_matrix/scrolltext.py)

This example displays scrolling text messages across one or more TheMatrix
boards:

    the_matrix_scrolltext Hello, world!

By default, it uses I2C address `0x30` but you can specify an address with the
`-a` option:

    the_matrix_scrolltext -a 0x37 'hello again'

If you've got more than one TheMatrix board connected to make a wider display,
specify their addresses in order and separated by commas for the script to
scroll the message across them together:

    the_matrix_scrolltext -a 0x30,0x37 "here's a longer message to scroll"

## Web Interface - [the_matrix_web](./the_matrix/web.py)

This is a very basic web interface for controlling TheMatrix. It runs on the
Raspberry Pi and uses the code described above. It needs Flask to run,
which should have been installed when you installed the module with `pip`.

To start the application, just run it:

    the_matrix_web

and visit your Raspberry Pi's IP address or hostname on port 5000 in your
browser. The application lets you control individual LEDS, rows and columns of
them together and vary the LED current.
