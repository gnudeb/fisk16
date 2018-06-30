
class Pointer:
    def __init__(self, ram, address, size):
        self.ram = ram
        self.address = address
        self.size = size

    def read(self):
        return self.ram.read(self.address, self.size)

    def write(self, value):
        self.ram.write(self.address, value, self.size)


class ImmediatePointer(int):
    def read(self):
        return self


def as_nibbles(byte):
    high = byte >> 4
    low = byte & 0x0f
    return high, low


def r16_r16(cpu):
    target_id, source_id = as_nibbles(cpu.ram[cpu.ip])
    target_ptr = Pointer(cpu.register_ram, target_id*2, 2)
    source_ptr = Pointer(cpu.register_ram, source_id*2, 2)
    cpu.ip += 1
    return target_ptr, source_ptr


def r16_ind(cpu):
    target_id, source_id = as_nibbles(cpu.ram[cpu.ip])
    target_ptr = Pointer(cpu.register_ram, target_id * 2, 2)
    pointer = cpu.register_ram.read(source_id*2, 2)
    source_ptr = Pointer(cpu.ram, pointer, 2)
    cpu.ip += 1
    return target_ptr, source_ptr


def ind_r16(cpu):
    target_id, source_id = as_nibbles(cpu.ram[cpu.ip])
    source_ptr = Pointer(cpu.register_ram, source_id * 2, 2)
    pointer = cpu.register_ram.read(target_id*2, 2)
    target_ptr = Pointer(cpu.ram, pointer, 2)
    cpu.ip += 1
    return target_ptr, source_ptr


def r8_r8(cpu):
    target_id, source_id = as_nibbles(cpu.ram[cpu.ip])
    target_ptr = Pointer(cpu.register_ram, target_id, 1)
    source_ptr = Pointer(cpu.register_ram, source_id, 1)
    cpu.ip += 1
    return target_ptr, source_ptr


def r8_ind(cpu):
    target_id, source_id = as_nibbles(cpu.ram[cpu.ip])
    target_ptr = Pointer(cpu.register_ram, target_id, 1)
    pointer = cpu.register_ram.read(source_id*2, 2)
    source_ptr = Pointer(cpu.ram, pointer, 1)
    cpu.ip += 1
    return target_ptr, source_ptr


def ind_r8(cpu):
    target_id, source_id = as_nibbles(cpu.ram[cpu.ip])
    source_ptr = Pointer(cpu.register_ram, source_id, 1)
    pointer = cpu.register_ram.read(target_id*2, 2)
    target_ptr = Pointer(cpu.ram, pointer, 1)
    cpu.ip += 1
    return target_ptr, source_ptr


def r16_imm16(cpu):
    target_id, _ = as_nibbles(cpu.ram[cpu.ip])
    target_ptr = Pointer(cpu.register_ram, target_id*2, 2)

    cpu.ip += 1
    immediate = cpu.ram[cpu.ip] * 256
    cpu.ip += 1
    immediate += cpu.ram[cpu.ip]
    source_ptr = ImmediatePointer(immediate)

    cpu.ip += 1
    return target_ptr, source_ptr


def r8_imm8(cpu):
    target_id, _ = as_nibbles(cpu.ram[cpu.ip])
    target_ptr = Pointer(cpu.register_ram, target_id, 1)

    cpu.ip += 1
    immediate = cpu.ram[cpu.ip]
    source_ptr = ImmediatePointer(immediate)

    cpu.ip += 1
    return target_ptr, source_ptr


def r16(cpu):
    target_id, _ = as_nibbles(cpu.ram[cpu.ip])
    cpu.ip += 1
    return Pointer(cpu.register_ram, target_id * 2, 2),


def imm16(cpu):
    immediate = cpu.ram[cpu.ip] * 256
    cpu.ip += 1
    immediate += cpu.ram[cpu.ip]
    cpu.ip += 1
    return ImmediatePointer(immediate),


def imm8(cpu):
    immediate = cpu.ram[cpu.ip]
    cpu.ip += 1
    return ImmediatePointer(immediate),


def mov(cpu, target: Pointer, source: Pointer):
    target.write(source.read())


def _or(cpu, target: Pointer, source: Pointer):
    target.write(target.read() | source.read())
    result = target.read()

    cpu.register_ram.write_bit('c', 0)
    cpu.register_ram.write_bit('z', not result)


def _and(cpu, target: Pointer, source: Pointer):
    target.write(target.read() & source.read())
    result = target.read()

    cpu.register_ram.write_bit('c', 0)
    cpu.register_ram.write_bit('z', not result)


def xor(cpu, target: Pointer, source: Pointer):
    target.write(target.read() ^ source.read())
    result = target.read()

    cpu.register_ram.write_bit('c', 0)
    cpu.register_ram.write_bit('z', not result)


def add(cpu, target: Pointer, source: Pointer):
    result = target.read() + source.read()
    target.write(result)

    cpu.register_ram.write_bit('c', result >= 1 << (target.size * 8))
    cpu.register_ram.write_bit('z', not result)


def addc(cpu, target: Pointer, source: Pointer):
    result = target.read() + source.read() + cpu.register_ram.read_bit('c')
    target.write(result)

    cpu.register_ram.write_bit('c', result >= 1 << (target.size * 8))
    cpu.register_ram.write_bit('z', not result)


def sub(cpu, target: Pointer, source: Pointer):
    result = target.read() - source.read()
    target.write(result)

    cpu.register_ram.write_bit('c', result < 0)
    cpu.register_ram.write_bit('z', not result)


def subc(cpu, target: Pointer, source: Pointer):
    result = target.read() - source.read() - cpu.register_ram.read_bit('c')
    target.write(result)

    cpu.register_ram.write_bit('c', result < 0)
    cpu.register_ram.write_bit('z', not result)


def xch(cpu, target: Pointer, source: Pointer):
    temp = source.read()
    source.write(target.read())
    target.write(temp)


def jz(cpu, target: Pointer):
    if not cpu.register_ram.read_bit('z'):
        return

    byte_offset = target.read()
    # Check whether offset is negative in two's complement (i.e. MSB is set)
    if byte_offset >> 7:
        # Compute true negative value
        byte_offset = -(-byte_offset % 256)

    cpu.ip += byte_offset


def cmp(cpu, target: Pointer, source: Pointer):
    # Basically a `sub` instruction without actual subtraction
    result = target.read() - source.read()

    cpu.register_ram.write_bit('c', result < 0)
    cpu.register_ram.write_bit('z', not result)


def test(cpu, target: Pointer):
    result = target.read()
    operand_size = target.size * 8

    # Carry bit is set if operand is negative
    cpu.register_ram.write_bit('c', result >> (operand_size - 1))
    cpu.register_ram.write_bit('z', not result)


def push(cpu, target: Pointer):
    value = target.read()

    cpu.ram[cpu.sp] = value & 0xff
    cpu.sp -= 1
    value >>= 8
    cpu.ram[cpu.sp] = value
    cpu.sp -= 1


def pop(cpu, target: Pointer):
    cpu.sp += 1
    value = cpu.ram[cpu.sp] << 8
    cpu.sp += 1
    value += cpu.ram[cpu.sp]

    target.write(value)


def call(cpu, target: Pointer):
    push(cpu, ImmediatePointer(cpu.ip))
    cpu.ip = target.read()

