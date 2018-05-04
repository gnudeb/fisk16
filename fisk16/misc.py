
class IndirectOperand:
    def __init__(self, operand, cpu):
        self.operand = operand
        self.cpu = cpu

    @property
    def value(self):
        address = self.operand.value
        return self.cpu.read(address)

    @value.setter
    def value(self, data):
        address = self.operand.value
        self.cpu.write(self.operand.value, address)
