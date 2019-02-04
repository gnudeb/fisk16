
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

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            self._set_slice(value, key.start, key.stop)
        elif isinstance(key, int):
            self._set_bit(value, key)
        else:
            raise ValueError(f"Unsupported type: {type(key)}")

    # TODO: Implement `from_dict(d: dict)`

    # TODO: Possibly rewrite using dict with `slice`s to eliminate redundancy

    @property
    def opcode(self):
        return self[15:12]

    @opcode.setter
    def opcode(self, value):
        self[15:12] = value

    @property
    def register_a(self):
        return self[11:8]

    @register_a.setter
    def register_a(self, value):
        self[11:8] = value

    @property
    def register_b(self):
        return self[7:4]

    @register_b.setter
    def register_b(self, value):
        self[7:4] = value

    @property
    def register_c(self):
        return self[3:0]

    @register_c.setter
    def register_c(self, value):
        self[3:0] = value

    @property
    def operation(self):
        return self[3:0]

    @operation.setter
    def operation(self, value):
        self[3:0] = value

    @property
    def short_operation(self):
        return self[3:1]

    @short_operation.setter
    def short_operation(self, value):
        self[3:1] = value

    @property
    def negate(self):
        return self[0]

    @negate.setter
    def negate(self, value):
        self[0] = value

    @property
    def imm8(self):
        return self[7:0]

    @imm8.setter
    def imm8(self, value):
        self[7:0] = value

    @property
    def imm4(self):
        return self[3:0]

    @imm4.setter
    def imm4(self, value):
        self[3:0] = value

    def _slice(self, start, stop):
        start, stop = min(start, stop), max(start, stop)
        size = stop - start + 1
        return (self.value >> start) & (0xFFFF >> (16 - size))

    def _bit(self, offset):
        return (self.value >> offset) & 1

    def _set_slice(self, value, start, stop):
        start, stop = min(start, stop), max(start, stop)

        # TODO: Implement `bit_mask()` function
        mask = (0xFFFF >> (15 - stop)) & (0xFFFF << start)
        self.value &= ~mask
        self.value |= value << start

    def _set_bit(self, value, offset):
        self.value &= ~(1 << offset)
        self.value |= value << offset
