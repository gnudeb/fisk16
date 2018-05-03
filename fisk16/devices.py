

class BaseDevice:
    def read(self, address):
        return 0

    def write(self, address, byte):
        pass


class DummyDevice(BaseDevice):
    pass


class ROMDevice(BaseDevice):
    def __init__(self, rom=None):
        self.rom = bytearray(4 * 1024)
        if rom:
            for i, byte in enumerate(rom):
                self.rom[i] = rom[i]

    def read(self, address):
        return self.rom[address]

    def write(self, address, byte):
        self.rom[address] = byte
