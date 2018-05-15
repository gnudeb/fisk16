
def mov(cpu, op1, op2):
    op1.value = op2.value


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
