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


class RegisterRAM(RAM):

    def __init__(self):
        # Fisk16 has 32 word-sized registers = 64 bytes
        super().__init__(32 * 2)
        self.pointers = {
            'r0':  (0 * 2, 2),
            'r1':  (1 * 2, 2),
            'r2':  (2 * 2, 2),
            'r3':  (3 * 2, 2),
            'r4':  (4 * 2, 2),
            'r5':  (5 * 2, 2),
            'r6':  (6 * 2, 2),
            'r7':  (7 * 2, 2),
            'r8':  (8 * 2, 2),
            'r9':  (9 * 2, 2),
            'r10': (10 * 2, 2),
            'r11': (11 * 2, 2),
            'r12': (12 * 2, 2),
            'r13': (13 * 2, 2),
            'r14': (14 * 2, 2),
            'ip':  (15 * 2, 2),
            'r0l': (0, 1),
            'r0h': (1, 1),
            'r1l': (2, 1),
            'r1h': (3, 1),
            'r2l': (4, 1),
            'r2h': (5, 1),
            'r3l': (6, 1),
            'r3h': (7, 1),
            'r4l': (8, 1),
            'r4h': (9, 1),
            'r5l': (10, 1),
            'r5h': (11, 1),
            'r6l': (12, 1),
            'r6h': (13, 1),
            'r7l': (14, 1),
            'r7h': (15, 1),
        }

    def read(self, address, size=1):
        if type(address) is str:
            address, size = self.pointers[address]
        return super().read(address, size)

    def write(self, address, value, size=1):
        if type(address) is str:
            address, size = self.pointers[address]
        super().write(address, value, size)


class Fisk16:

    def __init__(self):
        self.register_ram = RegisterRAM()
        self.ram = RAM(32)

    @property
    def ip(self):
        return self.register_ram.read('ip')

    @ip.setter
    def ip(self, value):
        self.register_ram.write('ip', value)

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

