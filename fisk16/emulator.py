from ctypes import c_uint8 as uint8,\
    c_uint16 as uint16

from .devices import DummyDevice
from .instructions import handlers as _handlers


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

        self.handlers = _handlers

    def tick(self):
        opcode = self.read(self.pc)
        handler = self.handlers[opcode]
        handler(self)

    def read(self, address=None):
        if not address:
            address = self.pc
        return self.device_at(address).read(address)

    def write(self, address, byte):
        adjusted_address = address & 0x0fff
        self.device_at(address).write(adjusted_address, byte)

    def device_at(self, address):
        return self.devices[address >> 12]

    def register(self, _id, byte_sized=False) -> Register16:
        if not byte_sized:
            return self.registers[_id]
        else:
            return self.registers[_id >> 1][_id & 1]
