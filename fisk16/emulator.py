from .instruction_set import instruction_set
from .misc import hexdump


class RAM(bytearray):

    def __str__(self):
        return hexdump(self)

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

    def read_bit(self, bit_offset):
        byte_offset = bit_offset >> 3
        local_bit_offset = bit_offset & 0b111
        byte = self[byte_offset]
        return bool(byte & (1 << local_bit_offset))

    def write_bit(self, bit_offset, bit):
        byte_offset = bit_offset >> 3
        local_bit_offset = bit_offset & 0b111
        byte = self[byte_offset]
        if bit == 0:
            byte &= (255 ^ (1 << local_bit_offset))
        else:
            byte |= (1 << local_bit_offset)
        self[byte_offset] = byte

    def write_bytes(self, address, it):
        for offset, byte in enumerate(it):
            self[address + offset] = byte


class RegisterRAM(RAM):
    pointers = {
        'r0': (0 * 2, 2),
        'r1': (1 * 2, 2),
        'r2': (2 * 2, 2),
        'r3': (3 * 2, 2),
        'r4': (4 * 2, 2),
        'r5': (5 * 2, 2),
        'r6': (6 * 2, 2),
        'r7': (7 * 2, 2),
        'r8': (8 * 2, 2),
        'r9': (9 * 2, 2),
        'r10': (10 * 2, 2),
        'r11': (11 * 2, 2),
        'r12': (12 * 2, 2),
        'sp': (13 * 2, 2),
        'fl': (14 * 2, 2),
        'ip': (15 * 2, 2),
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

    bit_pointers = {
        'c': ((14*2 + 1) * 8 + 0),  # bit 0 of 'fl' register -- Carry
        'z': ((14*2 + 1) * 8 + 1),  # bit 1 of 'fl' register -- Zero
    }

    def __init__(self):
        # Fisk16 has 32 word-sized registers = 64 bytes
        super().__init__(32 * 2)

    def read(self, address, size=1):
        if type(address) is str:
            address, size = self.pointers[address]
        return super().read(address, size)

    def write(self, address, value, size=1):
        if type(address) is str:
            address, size = self.pointers[address]
        super().write(address, value, size)

    def read_bit(self, bit_offset):
        if type(bit_offset) is str:
            bit_offset = self.bit_pointers[bit_offset]
        return super().read_bit(bit_offset)

    def write_bit(self, bit_offset, bit):
        if type(bit_offset) is str:
            bit_offset = self.bit_pointers[bit_offset]
        super().write_bit(bit_offset, bit)


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

    @property
    def sp(self):
        return self.register_ram.read('sp')

    @sp.setter
    def sp(self, value):
        self.register_ram.write('sp', value)

    def tick(self):
        opcode = self.ram[self.ip]
        self.ip += 1
        instruction, addressing_mode = instruction_set[opcode]

        instruction(self, *addressing_mode(self))
