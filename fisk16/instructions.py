from ctypes import c_uint8 as uint8,\
    c_uint16 as uint16

from .misc import IndirectOperand

def nop(cpu):
    cpu.pc += 1


def mov(cpu):
    cpu.pc += 1
    mod = cpu.read()
    addressing_mode = (mod & 0b01110000) >> 4
    op1_id = mod & 0b00001111

    if addressing_mode == 0:    # r8, r8
        cpu.pc += 1
        op2_id = cpu.read()

        op1 = cpu.register(op1_id, byte_sized=True)
        op2 = cpu.register(op2_id, byte_sized=True)
    elif addressing_mode == 1:  # r8, imm8
        cpu.pc += 1
        imm8 = cpu.read()

        op1 = cpu.register(op1_id, byte_sized=True)
        op2 = uint8(imm8)
    elif addressing_mode == 2:  # r16, r16
        cpu.pc += 1
        op2_id = cpu.read()

        op1 = cpu.register(op1_id)
        op2 = cpu.register(op2_id)
    elif addressing_mode == 3:  # r16, imm16
        cpu.pc += 1
        imm16 = cpu.read()
        cpu.pc += 1
        imm16 |= cpu.read() << 8

        op1 = cpu.register(op1_id)
        op2 = uint16(imm16)
    elif addressing_mode == 4:  # r8, [r16]
        cpu.pc += 1
        op2_id = cpu.read()

        op1 = cpu.register(op1_id, byte_sized=True)
        op2 = IndirectOperand(cpu.register(op2_id), cpu)
    elif addressing_mode == 5:  # [r16], imm8
        cpu.pc += 1
        imm8 = cpu.read()

        op1 = IndirectOperand(cpu.register(op1_id), cpu)
        op2 = uint8(imm8)
    elif addressing_mode == 6:  # [r16], r8
        cpu.pc += 1
        op2_id = cpu.read()

        op1 = IndirectOperand(cpu.register(op1_id), cpu)
        op2 = cpu.register(op2_id, byte_sized=True)
    else:
        raise Exception

    op1.value = op2.value


handlers = {
    0b00000000: nop,
    0b00000100: mov,
}

