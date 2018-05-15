from .instructions import (
    r16_r16, r16_ind, ind_r16, r8_r8, r8_ind, ind_r8, r16_imm16, r8_imm8,
    mov, _or,
)


class Instruction:
    def __init__(self, instruction, operand_provider=None):
        self.instruction = instruction
        self.operand_provider = operand_provider or (lambda cpu: tuple())

    def execute(self, cpu):
        operands = self.operand_provider(cpu)
        self.instruction(cpu, *operands)


I = Instruction
handlers = {
    0x00: I(mov, r16_r16),
    0x01: I(mov, r16_ind),
    0x02: I(mov, ind_r16),
    0x03: I(mov, r8_r8),
    0x04: I(mov, r8_ind),
    0x05: I(mov, ind_r8),
    0x06: I(mov, r16_imm16),
    0x07: I(mov, r8_imm8),
    0x08: I(_or, r16_r16),
    0x09: I(_or, r8_r8),
    0x0a: I(_or, r16_imm16),
    0x0b: I(_or, r8_imm8),
    # 0x0c: i.and_r16_r16,
    # 0x0d: i.and_r8_r8,
    # 0x0e: i.and_r16_imm16,
    # 0x0f: i.and_r8_imm8,
    # 0x10: i.add_r16_r16,
    # 0x11: i.add_r16_imm16,
}
