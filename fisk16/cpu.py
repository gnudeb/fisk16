from abc import ABC


class CPU(ABC):

    def read_register(self, register: int) -> int:
        pass

    def write_register(self, register: int, value: int):
        pass

    def read_byte(self, address: int) -> int:
        pass

    def write_byte(self, address: int, value: int):
        pass

    def read_word(self, address: int) -> int:
        pass

    def write_word(self, address: int, value: int):
        pass
