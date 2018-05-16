from .instructions import (
    r16_r16, r16_ind, ind_r16, r8_r8, r8_ind, ind_r8, r16_imm16, r8_imm8, r16, r8, imm16, imm8,
    mov, _or, _and, xor, add, addc, sub, subc, xch, cmp,
)


class OpcodeHandler:
    def __init__(self, instruction, operand_provider=None):
        self.instruction = instruction
        self.operand_provider = operand_provider or (lambda cpu: tuple())

    def execute(self, cpu):
        operands = self.operand_provider(cpu)
        if type(operands) is tuple:
            self.instruction(cpu, *operands)
        else:
            self.instruction(cpu, operands)


I = OpcodeHandler
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
    0x0c: I(_and, r16_r16),
    0x0d: I(_and, r8_r8),
    0x0e: I(_and, r16_imm16),
    0x0f: I(_and, r8_imm8),
    0x10: I(xor, r16_r16),
    0x11: I(xor, r8_r8),
    0x12: I(xor, r16_imm16),
    0x13: I(xor, r8_imm8),
    0x14: I(add, r16_r16),
    0x15: I(add, r8_r8),
    0x16: I(add, r16_imm16),
    0x17: I(add, r8_imm8),
    0x18: I(addc, r16_r16),
    0x19: I(addc, r8_r8),
    0x1a: I(addc, r16_imm16),
    0x1b: I(addc, r8_imm8),
    0x1c: I(sub, r16_r16),
    0x1d: I(sub, r8_r8),
    0x1e: I(sub, r16_imm16),
    0x1f: I(sub, r8_imm8),
    0x20: I(subc, r16_r16),
    0x21: I(subc, r8_r8),
    0x22: I(subc, r16_imm16),
    0x23: I(subc, r8_imm8),
    0x24: I(xch, r16_r16),
    0x25: I(xch, r8_r8),
    0x26: I(cmp, r16_r16),
    0x27: I(cmp, r8_r8),
    0x28: I(cmp, r16_imm16),
    0x29: I(cmp, r8_imm8),
}
