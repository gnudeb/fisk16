from ctypes import c_uint8 as uint8


class Register16:
    def __init__(self):
        self.low_byte = uint8()
        self.high_byte = uint8()

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
