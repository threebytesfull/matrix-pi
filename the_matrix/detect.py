try:
    from smbus import SMBus
except:
    from .fake_smbus import SMBus

def detect(bus_number=1):
    bus = SMBus(bus_number)
    if hasattr(bus, 'is_fake'):
        return [0x30]

    addresses = [];
    for address in range(0x30, 0x38):
        try:
            result = bus.read_byte(address)
            addresses.append(address)
        except:
            next
    return addresses
