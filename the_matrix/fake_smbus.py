class SMBus(object):
    """Fake SMBus for debugging purposes"""
    is_fake = True

    def __init__(self, bus_number=1):
        print("BUS:INIT bus=%d" % bus_number)

    def write_byte_data(self, address, register, data):
        print("BUS:WRITE [0x%02X 0x%02X 0x%02X]" % (address, register, data))

    def read_byte(self, address):
        print("BUS:READ  [0x%02x]" % address)
