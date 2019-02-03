from .cpu import CPU
from .definitions import Opcode, Register, AluMode, BoolMode
from .exceptions import MalformedInstruction
from .instruction import Instruction


class Fisk16Handler:

    def __init__(self, cpu: CPU):
        self.cpu = cpu

    def handle(self, instr: Instruction):
        if instr.opcode == Opcode.PUSH:
            self._push(instr.register_a)
        elif instr.opcode == Opcode.POP:
            self._pop(instr.register_a)
        elif instr.opcode == Opcode.STORE:
            self._store(instr.register_a, instr.register_b, instr.imm4)
        elif instr.opcode == Opcode.LOAD:
            self._load(instr.register_a, instr.register_b, instr.imm4)
        elif instr.opcode == Opcode.BOOLEAN:
            self._boolean(
                instr.register_a, instr.register_b,
                instr.short_operation, instr.negate)
        elif instr.opcode == Opcode.ALU:
            self._alu(instr.register_a, instr.register_b, instr.operation)
        elif instr.opcode == Opcode.ADD_IMMEDIATE:
            self._add_immediate(instr.register_a, instr.imm8)
        elif instr.opcode == Opcode.MOVE_IMMEDIATE:
            self._move_immediate(instr.register_a, instr.imm8)
        else:
            raise MalformedInstruction

    def _push(self, src_register):
        stack_pointer = self.cpu.read_register(Register.SP)
        src_value = self.cpu.read_register(src_register)
        self.cpu.write_word(stack_pointer, src_value)
        self.cpu.write_register(Register.SP, stack_pointer+2)

    def _pop(self, dest_register):
        stack_pointer = self.cpu.read_register(Register.Sp)
        dest_value = self.cpu.read_word(stack_pointer)
        self.cpu.write_register(dest_register, dest_value)

    def _alu(self, dest_register, src_register, mode: AluMode):
        dest_value = self.cpu.read_register(dest_register)
        src_value = self.cpu.read_register(src_register)

        # TODO: Implement all ALU modes according to spec
        if mode == AluMode.MOV:
            result = src_value
        elif mode == AluMode.OR:
            result = dest_value | src_value
        else:
            raise MalformedInstruction

        self.cpu.write_register(dest_register, result)

    def _store(self, dest_register, src_register, offset):
        # TODO: sign extend 4-bit `offset` to 16 bits
        dest_address = self.cpu.read_register(dest_register)
        dest_address = (dest_address + offset) % 0xFFFF
        src_value = self.cpu.read_register(src_register)
        self.cpu.write_byte(dest_address, src_value)

    def _load(self, dest_register, src_register, offset):
        src_address = self.cpu.read_register(src_register)
        src_address = (src_address + offset) % 0xFFFF
        src_value = self.cpu.read_byte(src_address)
        self.cpu.write_register(dest_register, src_value)

    def _boolean(self, dest_register, src_register, mode: BoolMode, negate):
        result: bool

        dest_value = self.cpu.read_register(dest_register)
        src_value = self.cpu.read_register(src_register)

        if mode == BoolMode.SET_IF_EQUAL:
            result = dest_value == src_value
        elif mode == BoolMode.SET_IF_NEGATIVE:
            result = bool(src_value & 0x8000)
        elif mode == BoolMode.SET_IF_LESS_THAN:
            result = dest_value < src_value
        # TODO: Implement SET_IF_LESS_UNSIGNED
        elif mode == BoolMode.SET_IF_ZERO:
            result = src_value == 0
        else:
            raise MalformedInstruction

        self.cpu.write_register(dest_register, result)

    def _add_immediate(self, dest_register, value):
        # TODO: sign extend 8-bit `value` to 16 bits
        initial_value = self.cpu.read_register(dest_register)
        self.cpu.write_register(dest_register, initial_value + value)

    def _move_immediate(self, dest_register, value):
        dest_value = self.cpu.read_register(dest_register)
        dest_value &= 0xFF00
        dest_value |= value
        self.cpu.write_register(dest_register, dest_value)
