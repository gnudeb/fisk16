
def mov(cpu, op1, op2):
    op1.value = op2.value


def _or(cpu, op1, op2):
    op1.value |= op2.value


def _and(cpu, op1, op2):
    op1.value |= op2.value


def xor(cpu, op1, op2):
    op1.value ^= op2.value


def add(cpu, op1, op2):
    # TODO: Set carry flag when needed
    op1.value += op2.value


def addc(cpu, op1, op2):
    # TODO: Set carry flag when needed
    # TODO: Implement carry flag
    op1.value += op2.value


def sub(cpu, op1, op2):
    # TODO: Set carry flag when needed
    op1.value -= op2.value


def subc(cpu, op1, op2):
    # TODO: Set carry flag when needed
    # TODO: Implement carry flag
    op1.value -= op2.value


def xch(cpu, op1, op2):
    op1.value, op2.value = op2.value, op1.value


def cmp(cpu, op1, op2):
    # TODO: Set appropriate flags depending on the values of the operands
    pass


def r16_r16(cpu):
    return cpu.next_registers()


def r16_ind(cpu):
    reg_a, reg_b = cpu.next_registers()
    return reg_a, cpu.pointer(reg_b.value, byte_sized=False)


def ind_r16(cpu):
    reg_a, reg_b = cpu.next_registers()
    return cpu.pointer(reg_a.value, byte_sized=False), reg_b


def r8_r8(cpu):
    return cpu.next_registers(byte_sized=True)


def r8_ind(cpu):
    reg_a, reg_b = cpu.next_registers(byte_sized=[True, False])
    return reg_a, cpu.pointer(reg_b.value)


def ind_r8(cpu):
    reg_a, reg_b = cpu.next_registers(byte_sized=[True, False])
    return cpu.pointer(reg_a.value), reg_b


def r16_imm16(cpu):
    reg_a = cpu.next_register()
    imm16 = cpu.next_word()

    return reg_a, imm16


def r8_imm8(cpu):
    reg_a = cpu.next_register(byte_sized=True)
    imm8 = cpu.next_byte()

    return reg_a, imm8


def r16(cpu):
    return cpu.next_register()


def r8(cpu):
    return cpu.next_register(byte_sized=True)


def imm16(cpu):
    return cpu.next_word()


def imm8(cpu):
    return cpu.next_byte()
