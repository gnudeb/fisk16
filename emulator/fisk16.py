from .cpu import CPU
from .definitions import Register
from .devices import Device, RAM
from .exceptions import UnprivilegedAccess
from .handlers import Fisk16Handler
from .types import Word
from .instruction import Instruction


class Fisk16(CPU):

    def __init__(self, handler_cls=Fisk16Handler):
        self._registers = [Word() for _ in range(32)]
        self._memory = bytearray(64)
        self._handler = handler_cls(self)
        self._devices = {
            0: RAM()
        }

    def tick(self):
        """
        Performs next instruction in memory, leaving CPU in a valid state.

        If some underlying operation (e.g. privileged register access)
        throws exception, this method handles it according to Fisk16 spec.
        """
        instruction = self._fetch_instruction()
        # TODO: Handle exceptions coming from `self.handle`
        self.handle(instruction)
        # TODO: Check for PC overflow

    def read_register(self, register: int) -> int:
        return self._registers[register].value

    def write_register(self, register: int, value: int):
        """
        Write `value` to register number `register`.

        If `value` is the same as the value present in register, access check
        is not performed.
        """
        if self._registers[register].value == value:
            return

        self._ensure_access(register)
        self._registers[register].value = value

    def read_byte(self, segment: int, address: int) -> int:
        # return self._memory[address]
        return self._device_at(segment).read(address)

    def write_byte(self, segment: int, address: int, value: int):
        # self._memory[address] = value
        self._device_at(segment).write(address, value)

    def read_word(self, segment: int, address: int) -> int:
        value = self.read_byte(segment, address) << 8
        value |= self.read_byte(segment, address + 1)
        return value

    def write_word(self, segment: int, address: int, value: int):
        self.write_byte(segment, address, value >> 8)
        self.write_byte(segment, address+1, value & 0xFF)

    def handle(self, instruction: Instruction):
        self._handler.handle(instruction)

    def _fetch_instruction(self) -> Instruction:
        code_segment = self.read_register(Register.CS)
        program_counter = self.read_register(Register.PC)
        value = self.read_word(code_segment, program_counter)

        self.write_register(Register.PC, program_counter + 2)

        return Instruction(value)

    def _ensure_access(self, register: int):
        bit_offset = register
        if self._registers[Register.PF][bit_offset] == 1:
            raise UnprivilegedAccess

    def _device_at(self, segment: int) -> Device:
        return self._devices[segment]
