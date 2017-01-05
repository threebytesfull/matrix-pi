class Layout(object):
    """Class to represent the layout of an AS1130 matrix"""

    def __init__(self, width=24, height=5, reversed=False):
        assert(width in [24, 12])
        assert(height == (5 if width==24 else 11))
        assert(reversed in ([True,False] if width == 24 else [False]))
        self._width = width
        self._height = height
        self._reversed = reversed
        self._connections = None
        self._mappedLayout = None

    @property
    def width(self):
        """Number of columns in LED matrix"""
        return self._width

    @property
    def height(self):
        """Number of rows in LED matrix"""
        return self._height

    @property
    def reversed(self):
        """Flag to indicate all LEDs connected in reverse"""
        return self._reversed

    @property
    def connections(self):
        """Connection pairs for each LED in coordinate grid"""
        if self._connections is None:
            # get connection pairs
            w = 10 if self.width == 24 else 11
            conn = [(anode, cathode) for cathode in range(12) for anode in [a for a in range(12) if a!= cathode][:w]]
            # arrange connection pairs in coordinate grid
            col_height, cols = (5, 24) if self.width == 24 else (11, 12)
            self._connections = [conn[col_height*i:col_height*i+col_height] for i in range(cols)]
        return self._connections

    def ledAt(self, x, y):
        """Returns the number of the LED at the specified coordinates"""
        assert(x in range(self.width))
        assert(y in range(self.height))
        anode, cathode = self.connections[x][y]
        if self.reversed:
            if self._mappedLayout == None:
                self._mappedLayout = Layout(12, 11)
            mappedX = anode
            mappedY = self._mappedLayout.connections[anode].index((cathode, anode))
            number = self._mappedLayout.ledAt(mappedX, mappedY)
        else:
            number = 16*cathode + y + (5*(x % 2) if self.width == 24 else 0)
        return number

    def numToAddressOnOff(self, led_number):
        """Returns the on/off address details (byte and bit) of the LED with the specified number"""
        hi, lo = ((led_number >> 4) & 0xf), (led_number & 0xf)
        assert(hi in range(12))
        assert(lo in range(11))
        byte_offset = int(lo/8) # later bits in second byte
        address_byte = 2*hi + int(lo/8)
        address_bit = lo % 8
        return (address_byte, address_bit)

    def numToAddressBlink(self, led_number):
        """Returns the blink address details (byte and bit) of the LED with the specified number"""
        hi, lo = ((led_number >> 4) & 0xf), (led_number & 0xf)
        assert(hi in range(12))
        assert(lo in range(11))
        byte_offset = int(lo/8) # later bits in second byte
        address_byte = 2*hi + int(lo/8)
        address_bit = lo % 8
        return (address_byte, address_bit)

    def numToAddressPWM(self, led_number):
        """Returns the PWM address details (byte) of the LED with the specified number"""
        hi, lo = ((led_number >> 4) & 0xf), (led_number & 0xf)
        assert(hi in range(12))
        assert(lo in range(11))
        address_byte = 0x18 + 11*hi + lo
        return address_byte
