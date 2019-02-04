
class Instruction:
    """
    A Fisk 16 instruction.

    This class is a wrapper around 16-bit value, that provides a convenient
    way to read and write various bit fields.

    For example, highest 4 bits (from 12 to 15, inclusive) are defined by
    Fisk 16 specification to store the value of opcode:

    >>> i = Instruction(0b1001_0000_0000_0000)
    >>> print(bin(i.opcode))
    0b1001

    You can also manually subscript `Instruction` objects:

    >>> i = Instruction(0b1001_0000_0000_0000)
    >>> print(bin(i[12:15]))
    0b1001
    >>> print(bin(i[15:12]))    # Bit boundaries are reversed
    0b1001
    """

    def __init__(self, value: int):
        self.value = value

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._slice(item.start, item.stop)
        if isinstance(item, int):
            return self._bit(item)

        raise ValueError(f"Unsupported type: {type(item)}")

    @property
    def opcode(self):
        return self[15:12]

    @property
    def register_a(self):
        return self[11:8]

    @property
    def register_b(self):
        return self[7:4]

    @property
    def register_c(self):
        return self[3:0]

    @property
    def operation(self):
        return self[3:0]

    @property
    def short_operation(self):
        return self[3:1]

    @property
    def negate(self):
        return self[0]

    @property
    def imm8(self):
        return self[7:0]

    @property
    def imm4(self):
        return self[3:0]

    def _slice(self, start, stop):
        start, stop = min(start, stop), max(start, stop)
        size = stop - start + 1
        return (self.value >> start) & (0xFFFF >> (16 - size))

    def _bit(self, offset):
        return (self.value >> offset) & 1
