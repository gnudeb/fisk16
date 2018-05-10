from .helpers import fetch_register, fetch_registers


def mov_r16_r16(cpu):
    reg_a, reg_b = fetch_registers(cpu)
    reg_a.value = reg_b.value


def mov_r16_ind(cpu):
    reg_a, reg_b = fetch_registers(cpu)

    address = reg_b.value
    reg_a.value = cpu.read(address, count=2)


def mov_ind_r16(cpu):
    reg_a, reg_b = fetch_registers(cpu)

    address = reg_a.value
    cpu.write(address, reg_b.value, count=2)


def mov_r8_r8(cpu):
    reg_a, reg_b = fetch_registers(cpu, byte_sized=True)
    reg_a.value = reg_b.value


def mov_r8_ind(cpu):
    reg_a, reg_b = fetch_registers(cpu, byte_sized=[True, False])

    address = reg_b.value
    reg_a.value = cpu.read(address)


def mov_ind_r8(cpu):
    reg_a, reg_b = fetch_registers(cpu, byte_sized=[False, True])

    address = reg_a.value
    cpu.write(address, reg_b.value)


def mov_r16_imm16(cpu):
    reg_a = fetch_register(cpu)
    imm16 = cpu.next_word()

    reg_a.value = imm16
