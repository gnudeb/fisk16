
class Pointer:
    def __init__(self, cpu, address, size=1):
        self.cpu = cpu
        self.address = address
        self.size = size

    @property
    def value(self):
        return self.cpu.read(self.address, self.size)

    @value.setter
    def value(self, number):
        self.cpu.write(self.address, number, self.size)


def nibbles(byte):
    low_nibble = byte & 0b00001111
    high_nibble = (byte & 0b11110000) >> 4

    return high_nibble, low_nibble

