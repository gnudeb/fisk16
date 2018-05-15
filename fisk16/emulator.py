from .devices import DummyDevice
from .opcode_handlers import handlers as _handlers
from .types import uint8, uint16, Pointer, Register16


class Fisk16:
    def __init__(self, instructions=None):
        self.pc = Register16()
        self.sp = Register16()
        self.registers = [Register16() for _ in range(16)]
        self.devices = [DummyDevice() for _ in range(16)]

        self.handlers = _handlers

    def tick(self):
        opcode = self.next_byte().value
        opcode_handler = self.handlers[opcode]
        opcode_handler.execute(self)

    def read(self, address=None, byte_sized=True):
        if not address:
            address = self.pc.value

        value = self.device_at(address).read(address)
        if not byte_sized:
            address += 1
            second_byte = self.device_at(address).read(address)
            value += second_byte << 8

        return value

    def write(self, address, number, byte_sized=True):
        if byte_sized:
            self.device_at(address).write(address, number)
        else:
            low_byte = number & 0x0f
            high_byte = (number & 0xf0) >> 8
            self.device_at(address).write(address, low_byte)
            address += 1
            self.device_at(address).write(address, high_byte)

    def device_at(self, address):
        return self.devices[address >> 12]

    def register(self, _id, byte_sized=False) -> Register16:
        if not byte_sized:
            # registers[abcd]
            return self.registers[_id]
        else:
            # registers[abc][d]
            return self.registers[_id >> 1][_id & 1]

    def next_byte(self) -> uint8:
        byte = self.read()
        self.pc.value += 1
        return uint8(byte)

    def next_word(self) -> uint16:
        word = self.read(byte_sized=False)
        self.pc.value += 2
        return uint16(word)

    def pointer(self, address, byte_sized=True):
        return Pointer(self, address, byte_sized)

    def next_registers(self, byte_sized=False):
        registers_byte = self.next_byte()
        reg_b_id, reg_a_id = registers_byte.nibbles()

        if type(byte_sized) is list:
            byte_sized_a, byte_sized_b = byte_sized
        else:
            byte_sized_a = byte_sized_b = byte_sized

        reg_a = self.register(reg_a_id, byte_sized=byte_sized_a)
        reg_b = self.register(reg_b_id, byte_sized=byte_sized_b)

        return reg_a, reg_b

    def next_register(self, byte_sized=False):
        registers_byte = self.next_byte()
        _, reg_a_id = registers_byte.nibbles()

        reg_a = self.register(reg_a_id, byte_sized=byte_sized)

        return reg_a
