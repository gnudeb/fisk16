
def nibbles(byte):
    low_nibble = byte & 0b00001111
    high_nibble = (byte & 0b11110000) >> 4

    return high_nibble, low_nibble


def fetch_registers(cpu, byte_sized=False):
    registers_byte = cpu.next_byte()
    reg_b_id, reg_a_id = nibbles(registers_byte)

    if type(byte_sized) is list:
        byte_sized_a, byte_sized_b = byte_sized
    else:
        byte_sized_a = byte_sized_b = byte_sized

    reg_a = cpu.register(reg_a_id, byte_sized=byte_sized_a)
    reg_b = cpu.register(reg_b_id, byte_sized=byte_sized_b)

    return reg_a, reg_b


def fetch_register(cpu, byte_sized=False):
    registers_byte = cpu.next_byte()
    _, reg_a_id = nibbles(registers_byte)

    reg_a = cpu.register(reg_a_id, byte_sized=byte_sized)

    return reg_a