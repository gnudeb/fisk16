from ctypes import c_uint8, c_uint16 as uint16


class uint8(c_uint8):
    def nibbles(self):
        byte = self.value
        low_nibble = byte & 0b00001111
        high_nibble = (byte & 0b11110000) >> 4

        return high_nibble, low_nibble
