#!/usr/bin/env python

import math, smbus, time

class TheMatrix():
    """Class to control Boldport 'The Matrix'"""
    class _register:
        nop             = 0x00
        on_off_frame    = 0x01
        blink_pwm_frame = 0x40
        dot_correction  = 0x80
        control         = 0xc0
        select          = 0xfd

    class _control:
        picture         = 0x00
        movie           = 0x01
        movie_mode      = 0x02
        frame_time      = 0x03
        display_option  = 0x04
        current_source  = 0x05
        config          = 0x06
        interrupt_mask  = 0x07
        interrupt_frame = 0x08
        shutdown        = 0x09
        i2c_monitor     = 0x0a
        clock_sync      = 0x0b
        interrupt_stat  = 0x0e
        status          = 0x0f
        open_led        = 0x20

    def __init__(self, address=0x30, bus_number=1):
        """Create TheMatrix object with specified I2C address and bus number"""
        self._address = address
        self._bus = smbus.SMBus(bus_number)

    def _writeCommand(self, register, subregister, data):
        self._bus.write_byte_data(self._address, self._register.select, register)
        self._bus.write_byte_data(self._address, subregister, data)

    def readByte(self, register, subregister):
        """Read byte from specified register and subregister"""
        self._bus.write_byte_data(self._address, self._register.select, reigster)
        self._bus.write_byte(self._address, subregister)
        return self._bus.read_byte(self._address)

    def reset(self):
        """Reset TheMatrix display driver chip"""
        self._writeCommand(self._register.control, self._control.shutdown, 0)
        time.sleep(0.005) # wait 5ms to chip to be ready

    def _configure(self,
            low_vdd_rst=0,
            low_vdd_stat=0,
            led_error_correction=0,
            dot_corr=0,
            common_addr=0,
            mem_conf=0):
        data = (
            (low_vdd_rst & 1) << 7 |
            (low_vdd_stat & 1) << 6 |
            (led_error_correction & 1) << 5 |
            (dot_corr & 1) << 4 |
            (common_addr & 1) << 3 |
            (mem_conf & 7)
        )
        self._writeCommand(self._register.control, self._control.config, data)

    def selectMemoryConfig(self, number=1):
        """Select RAM configuration"""
        self._configure(mem_conf=number)

    def setCurrentSource(self, mA=5):
        """Set current source (milliamps)"""
        assert(mA >= 0 and mA <= 30)
        data = int(mA*(255/30.0))
        self._writeCommand(self._register.control, self._control.current_source, data)

    def setDisplayOptions(self, loops=1, blink_freq=0, scan_limit=11):
        """Set display options"""
        data = (
            (loops & 7) << 5 |
            (blink_freq & 1) << 4 |
            (scan_limit & 15)
        )
        self._writeCommand(self._register.control, self._control.display_option, data)

    def displayPictureFrame(self, number=0, display=1, blink=0):
        """Display picture frame"""
        data = (
            (blink & 1) << 7 |
            (display & 1) << 6 |
            (number & 63)
        )
        self._writeCommand(self._register.control, self._control.picture, data)

    def display(self, on=1):
        """Set display on/off"""
        test_all = 0
        auto_test = 0
        manual_test = 0
        init = 1
        data = (
            (test_all & 1) << 4 |
            (auto_test & 1) << 3 |
            (manual_test & 1) << 2 |
            (init & 1) << 1 |
            (on & 1)
        )
        self._writeCommand(self._register.control, self._control.shutdown, data)

    def writeBlinkPWMFrame(self, number, frameData):
        """Write a blink/PWM frame to the specified frame number"""
        data = frameData.data
        for i in range(len(data)):
            self._writeCommand(self._register.blink_pwm_frame+number, i, data[i])

    def writeOnOffFrame(self, number, frameData):
        """Write an on/off frame to the specified frame number"""
        data = frameData.data
        for i in range(len(data)):
            self._writeCommand(self._register.on_off_frame+number, i, data[i])

    class OnOffFrame():
        def __init__(self, value=0, pwm=0):
            value &= 1
            byte0 = int(''.join([str(value) for i in range(8)]), 2)
            byte1 = byte0 & 3
            self._pixels = [byte0, byte1] * 12
            self.pwm = pwm

        @property
        def pwm(self):
            return (self._pixels[1] >> 5) & 7

        @pwm.setter
        def pwm(self, value):
            self._pixels[1] = (self._pixels[1] & 0x1f) | (value << 5)

        def setPixel(self, x, y, value=1):
            value &= 1
            segment = int(x/2)
            side = x % 2
            led = side*5 + y
            byte = int(led/8)
            addr = segment*2+byte
            bit = led % 8
            masked = 1 << bit
            if value == 1:
                self._pixels[addr] |= masked
            else:
                self._pixels[addr] &= ~masked & 255

        def getPixel(self, x, y):
            segment = int(x/2)
            side = x % 2
            led = side*5 + y
            byte = int(led/8)
            addr = segment*2+byte
            bit = led % 8
            value = (self._pixels[addr] >> bit) & 1
            return value

        @property
        def data(self):
            return self._pixels

        def __repr__(self):
            output = ''
            for y in range(5):
                for x in range(24):
                    value = self.getPixel(x, y)
                    output += '#' if value == 1 else '.'
                output += "\n"
            return output

    class BlinkPWMFrame():
        def __init__(self, blink=0, pwm=255):
            blink &= 1
            pwm &= 255
            blink_byte0 = int(''.join([str(blink) for i in range(8)]), 2)
            blink_byte1 = blink_byte0 & 3
            blink_bytes = [blink_byte0, blink_byte1] * 12
            pwm_bytes = [pwm] * 12*11
            self._data = blink_bytes + pwm_bytes

        @property
        def data(self):
            return self._data

        def setBlink(self, x, y, value=1):
            value &= 1
            segment = int(x/2)
            side = x % 2
            led = side*5 + y
            byte = int(led/8)
            addr = segment*2+byte
            bit = led % 8
            masked = 1 << bit
            if value == 1:
                self._data[addr] |= masked
            else:
                self._pixels[addr] &= ~masked & 255

        def setPWM(self, x, y, value=255):
            value &= 255
            segment = int(x/2)
            side = x % 2
            led = side*5 + y
            addr = 24 + segment*11 + side*5 + y
            self._data[addr] = value

def main():
    matrix = TheMatrix()
    matrix.reset()
    matrix.selectMemoryConfig(1)
    matrix.setCurrentSource(1)

    # write blink/pwm frame 0
    blinkPWMFrame = TheMatrix.BlinkPWMFrame()
    matrix.writeBlinkPWMFrame(0, blinkPWMFrame)

    # write on/off frame 0
    onOffFrame = TheMatrix.OnOffFrame(1) # new frame with all LEDs on
    matrix.writeOnOffFrame(0, onOffFrame)

    # set display options
    matrix.setDisplayOptions()

    # display picture frame 0
    matrix.displayPictureFrame(0)

    # display on
    matrix.display(1)

if __name__ == "__main__":
    main()
