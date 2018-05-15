from ctypes import c_uint8, c_uint16

uint16 = c_uint16


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


class Register16:
    def __init__(self):
        self.low_byte = c_uint8()
        self.high_byte = c_uint8()

    def __str__(self):
        return "0x{:02x}{:02x}".format(self.high_byte.value, self.low_byte.value)

    def __repr__(self):
        return "Register16({})".format(str(self))

    def __getitem__(self, item):
        if item == 0:
            return self.low_byte
        elif item == 1:
            return self.high_byte
        else:
            raise Exception

    @property
    def value(self):
        return (self.high_byte.value << 8) + self.low_byte.value

    @value.setter
    def value(self, word):
        self.high_byte.value = (word & 0xff00) >> 8
        self.low_byte.value = word & 0x00ff

    def set(self, word):
        self.high_byte.value = (word & 0xff00) >> 8
        self.low_byte.value = word & 0x00ff

    def get(self):
        return self.high_byte.value >> 8 + self.low_byte.value
