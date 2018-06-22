from .instruction_set import instruction_set

class RAM(bytearray):

    def __str__(self):
        output = ''
        for byte in self:
            output += '{:02x} '.format(byte)
        return output

    def read(self, address, size=1):
        value = 0
        for offset in range(size):
            value <<= 8
            value += self[address + offset]
        return value

    def write(self, address, value, size=1):
        for offset in range(size)[::-1]:
            self[address + offset] = value & 255
            value >>= 8


class Fisk16:

    def __init__(self):
        self.register_ram = RAM(32 * 2)
        self.ram = RAM(32)

    @property
    def ip(self):
        return self.register_ram.read(30, 2)

    @ip.setter
    def ip(self, value):
        self.register_ram.write(30, value, 2)

    @staticmethod
    def _as_nibbles(byte):
        high = byte >> 4
        low = byte & 0x0f
        return high, low

    def tick(self):
        opcode = self.ram[self.ip]
        self.ip += 1
        instruction, addressing_mode = instruction_set[opcode]

        instruction(self, *addressing_mode(self))

