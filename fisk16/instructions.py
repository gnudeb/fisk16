
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


def mov(cpu, target: Pointer, source: Pointer):
    target.write(source.read())


def _or(cpu, target: Pointer, source: Pointer):
    target.write(target.read() | source.read())


def _and(cpu, target: Pointer, source: Pointer):
    target.write(target.read() & source.read())


def xor(cpu, target: Pointer, source: Pointer):
    target.write(target.read() ^ source.read())


def add(cpu, target: Pointer, source: Pointer):
    target.write(target.read() + source.read())


def addc(cpu, target: Pointer, source: Pointer):
    # TODO: Implement carry bit
    target.write(target.read() + source.read())
