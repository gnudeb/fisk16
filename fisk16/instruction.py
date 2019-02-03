
class Instruction:

    def __init__(self, value: int):
        self.value = value

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._slice(item.start, item.stop)

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
    def imm8(self):
        return self[7:0]

    @property
    def imm4(self):
        return self[3:0]

    def _slice(self, start, stop):
        start, stop = min(start, stop), max(start, stop)
        size = stop - start + 1
        return (self.value >> start) & (0xFFFF >> (16 - size))
