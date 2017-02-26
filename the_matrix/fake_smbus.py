class SMBus(object):
    """Fake SMBus for debugging purposes"""
    is_fake = True

    def __init__(self, bus_number=1):
        print("BUS:INIT bus=%d" % bus_number)

    def write_byte_data(self, address, register, data):
        print("BUS:WRITE [0x%02X 0x%02X 0x%02X]" % (address, register, data))

    def write_i2c_block_data(self, address, register, data):
        print("BUS:WRITE_BLOCK [0x%02X 0x%02X %s]" % (address, register, ' '.join(list(map(lambda x: "%02X" % x, data)))))

    def read_byte(self, address):
        print("BUS:READ  [0x%02x]" % address)
