from .cpu import CPU
from .definitions import Register
from .exceptions import UnprivilegedAccess
from .handlers import Fisk16Handler
from .types import Word
from .instruction import Instruction


class Fisk16(CPU):

    register_alias = {
        "pc": Register.PC
    }

    def __init__(self, handler_cls=Fisk16Handler):
        self._registers = [Word() for _ in range(32)]
        self._memory = bytearray(64)
        self._handler = handler_cls(self)

    def __getattr__(self, key):
        if key in self.register_alias:
            register = self.register_alias[key]
            return self.read_register(register)

        raise AttributeError(f"'{type(self)}' has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key in self.register_alias:
            register = self.register_alias[key]
            self.write_register(register, value)
            return

        object.__setattr__(self, key, value)

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

    def read_byte(self, address: int) -> int:
        return self._memory[address]

    def write_byte(self, address: int, value: int):
        self._memory[address] = value

    def read_word(self, address: int) -> int:
        value = self.read_byte(address) << 8
        value |= self.read_byte(address + 1)
        return value

    def write_word(self, address: int, value: int):
        self.write_byte(address, value >> 8)
        self.write_byte(address+1, value & 0xFF)

    def handle(self, instruction: Instruction):
        self._handler.handle(instruction)

    def _fetch_instruction(self) -> Instruction:
        value = self._memory[self.pc] << 8
        self.pc += 1
        value += self._memory[self.pc]
        self.pc += 1

        return Instruction(value)

    def _ensure_access(self, register: int):
        bit_offset = register
        if self._registers[Register.PF][bit_offset] == 1:
            raise UnprivilegedAccess
