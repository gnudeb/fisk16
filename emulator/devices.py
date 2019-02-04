
class Device:

    def read(self, address: int) -> int:
        """Read a byte at `address` from this device."""
        raise NotImplementedError

    def write(self, address: int, value: int):
        """Write a byte `value` to an `address` on this device."""
        raise NotImplementedError


class RAM(Device):

    def __init__(self):
        self._memory = bytearray(0x10000)

    def read(self, address: int):
        return self._memory[address]

    def write(self, address: int, value: int):
        self._memory[address] = value
