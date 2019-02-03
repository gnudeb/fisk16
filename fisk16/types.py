
class Word:

    def __init__(self):
        self._value = 0

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._bit(key)
        elif isinstance(key, slice):
            return self._slice(key.start, key.stop)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._write_bit(key, value)
        elif isinstance(key, slice):
            self._write_slice(key.start, key.stop, value)

    def __repr__(self):
        return f"<Word {hex(self.value)}>"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value % 0x10000

    def _bit(self, offset) -> int:
        return (self.value >> offset) & 1

    def _slice(self, start, stop):
        start, stop = min(start, stop), max(start, stop)
        size = stop - start + 1
        return (self.value >> start) & (0xFFFF >> (16 - size))

    def _write_bit(self, offset, value):
        mask = 1 << offset

        if value == 0:
            self._value &= ~mask
        elif value == 1:
            self._value |= mask

    def _write_slice(self, start, stop, value):
        start, stop = min(start, stop), max(start, stop)
        slice_size = stop - start + 1

        mask = (0xFFFF >> (16 - slice_size)) << start
        self._value &= ~mask
        self._value |= value << start
