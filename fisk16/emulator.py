from .devices import DummyDevice
from .registers import Register16
from .opcode_handlers import handlers as _handlers


class Fisk16:
    def __init__(self, instructions=None):
        self.pc = Register16()
        self.sp = Register16()
        self.registers = [Register16() for _ in range(16)]
        self.devices = [DummyDevice() for _ in range(16)]

        self.handlers = _handlers

    def tick(self):
        opcode = self.next_byte()
        handler = self.handlers[opcode]
        handler(self)

    def read(self, address=None, count=1):
        if not address:
            address = self.pc.value

        value = 0
        for place in range(count):
            byte = self.device_at(address).read(address)
            value += byte << (8*place)
            address += 1
        return value

    def write(self, address, number, count=1):
        for place in range(count):
            adjusted_address = address & 0x0fff
            byte = number & 0xff
            self.device_at(address).write(adjusted_address, byte)
            number >>= 8
            address += 1

    def device_at(self, address):
        return self.devices[address >> 12]

    def register(self, _id, byte_sized=False) -> Register16:
        if not byte_sized:
            # registers[abcd]
            return self.registers[_id]
        else:
            # registers[abc][d]
            return self.registers[_id >> 1][_id & 1]

    def next_byte(self):
        byte = self.read()
        self.pc.value += 1
        return byte

    def next_word(self):
        word = self.read()
        self.pc.value += 1
        word += self.read() << 8
        self.pc.value += 1
        return word
