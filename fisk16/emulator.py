from ctypes import c_uint8 as uint8,\
    c_uint16 as uint16

from .devices import DummyDevice


def nop(cpu: 'Fisk16'):
    cpu.pc += 1


def mov(cpu: 'Fisk16'):
    cpu.pc += 1
    mod = cpu.read(cpu.pc)
    op1_id = mod & 0b00001111
    addressing_is_direct = not bool(mod & 0b01000000)
    has_immediate = bool(mod & 0b00010000)
    if addressing_is_direct:
        operands_are_word_sized = bool(mod & 0b00100000)
        if not operands_are_word_sized:
            op1 = cpu.register(op1_id, byte_sized=True)
            if not has_immediate:   # Addressing mode 000 (r8, r8)
                cpu.pc += 1
                op2_id = cpu.read(cpu.pc)
                op2 = cpu.register(op2_id, byte_sized=True)
            else:   # Addressing mode 001 (r8, imm8)
                cpu.pc += 1
                op2 = uint8(cpu.read(cpu.pc))
        else:
            op1 = cpu.register(op1_id)
            if not has_immediate:   # Addressing mode 010 (r16, r16)
                cpu.pc += 1
                op2_id = cpu.read(cpu.pc)
                op2 = cpu.register(op2_id)
            else:   # Addressing mode 011 (r16, imm16)
                cpu.pc += 1
                imm16 = cpu.read(cpu.pc)
                cpu.pc += 1
                imm16 |= cpu.read(cpu.pc) << 8
                op2 = uint16(imm16)

        op1.value = op2.value

    cpu.pc += 1


handlers = {
    0b00000000: nop,
    0b00000100: mov,
}


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


class Fisk16:
    def __init__(self):
        self.pc = 0
        self.sp = 0
        self.registers = [Register16() for _ in range(16)]
        self.devices = [DummyDevice() for _ in range(16)]

    def tick(self):
        opcode = self.read(self.pc)
        handler = handlers[opcode]
        handler(self)

    def read(self, address):
        return self.device_at(address).read(address)

    def device_at(self, address):
        return self.devices[address >> 12]

    def register(self, _id, byte_sized=False) -> Register16:
        if not byte_sized:
            return self.registers[_id]
        else:
            return self.registers[_id >> 1][_id & 1]
