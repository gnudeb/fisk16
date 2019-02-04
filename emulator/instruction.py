from .util import bit_mask


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

    fields = {
        "opcode": slice(12, 15),
        "register_a": slice(8, 11),
        "register_b": slice(4, 7),
        "register_c": slice(0, 3),
        "operation": slice(0, 3),
        "short_operation": slice(1, 3),
        "negate": 0,
        "imm8": slice(0, 7),
        "imm4": slice(0, 3),
    }

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

    def __getattr__(self, key):
        if key in self.fields:
            return self._field(key)

    def __setattr__(self, key, value):
        if key in self.fields:
            self._set_field(key, value)
        else:
            super().__setattr__(key, value)

    @classmethod
    def from_keywords(cls, **kw) -> 'Instruction':
        """
        Returns new instance of `Instruction` with fields according to `kw`.

        >>> i = Instruction.from_keywords(opcode=0b1111, register_a=0b1001)
        >>> print(i.opcode, i.register_a)
        15 9
        """
        return cls.from_dict(kw)

    @classmethod
    def from_dict(cls, d: dict):
        """
        Returns new instance of `Instruction` with fields according to dict.

        >>> i = Instruction.from_dict({"opcode": 0b1111, "register_a": 0b1001})
        >>> print(i.opcode, i.register_a)
        15 9
        """
        i = cls(0)
        for field, value in d.items():
            i._set_field(field, value)

        return i

    # TODO: Possibly rewrite using dict with `slice`s to eliminate redundancy

    def _slice(self, start, stop):
        start, stop = min(start, stop), max(start, stop)
        size = stop - start + 1
        return (self.value >> start) & (0xFFFF >> (16 - size))

    def _bit(self, offset):
        return (self.value >> offset) & 1

    def _set_slice(self, value, start, stop):
        start, stop = min(start, stop), max(start, stop)
        size = stop - start + 1

        value &= bit_mask(0, size)

        self.value &= ~bit_mask(start, stop)
        self.value |= value << start

    def _set_bit(self, value, offset):
        self.value &= ~(1 << offset)
        self.value |= value << offset

    def _field(self, name):
        key = self.fields[name]
        return self[key]

    def _set_field(self, name, value):
        key = self.fields[name]
        self[key] = value
