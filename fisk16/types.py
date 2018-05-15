from ctypes import c_uint8, c_uint16 as uint16


class uint8(c_uint8):
    def nibbles(self):
        byte = self.value
        low_nibble = byte & 0b00001111
        high_nibble = (byte & 0b11110000) >> 4

        return high_nibble, low_nibble


class Pointer:
    def __init__(self, cpu, address, byte_sized):
        self.cpu = cpu
        self.address = address
        self.byte_sized = byte_sized

    @property
    def value(self):
        return self.cpu.read(self.address, self.byte_sized)

    @value.setter
    def value(self, number):
        self.cpu.write(self.address, number, self.byte_sized)


