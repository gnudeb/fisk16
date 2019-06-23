# TODO: Rewrite using pytest

from emulator.definitions import Register, Opcode, AluMode
from emulator.exceptions import UnprivilegedAccess
from emulator.instruction import Instruction
from emulator.fisk16 import Fisk16
from emulator.types import Word
from emulator.util import sign_extend, bit_mask

import unittest


class Fisk16TestCase(unittest.TestCase):

    def setUp(self):
        self.fisk = Fisk16()

    def test_push_pop(self):
        register_value = 0xFA5F

        self.fisk.write_register(Register.R0, register_value)
        self.fisk.handle(Instruction.from_keywords(
            opcode=Opcode.PUSH, register_a=Register.R0))
        self.fisk.handle(Instruction.from_keywords(
            opcode=Opcode.POP, register_a=Register.R1))

        self.assertEqual(self.fisk.read_register(Register.R1), register_value)

    def test_call_return(self):
        call_destination = 0x8000

        initial_address = self.fisk.read_register(Register.PC)

        self.fisk.write_register(Register.R0, call_destination)
        self.fisk.handle(Instruction.from_keywords(
            opcode=Opcode.CALL, register_a=Register.CS, register_b=Register.R0))

        self.assertEqual(self.fisk.read_register(Register.PC), call_destination)

        self.fisk.handle(Instruction.from_keywords(
            opcode=Opcode.POP, register_a=Register.CS))
        self.fisk.handle(Instruction.from_keywords(
            opcode=Opcode.POP, register_a=Register.PC))

        # Note that in reality `pc` should be equal `initial_address + 2`
        # because fetch process would have incremented `pc` by 2 before
        # executing `call` instruction
        # `handle()` method assumes that it receives previously `fetch`ed
        # instruction
        # A better version of this test would be writing instruction values
        # directly to memory, and then calling `fisk.tick()` three times
        # TODO: Write a better version of this test ^
        self.assertEqual(
            self.fisk.read_register(Register.PC), initial_address)

    def test_unprivileged_access(self):
        self.fisk.write_register(Register.R0, 0)

        self.fisk.write_register(Register.PF, 1 << Register.R0)
        with self.assertRaises(UnprivilegedAccess):
            self.fisk.write_register(Register.R0, 1)

        self.fisk.write_register(Register.PF, 0)
        self.fisk.write_register(Register.R0, 2)

    def test_unprivileged_access_same_value(self):
        self.fisk.write_register(Register.R0, 0)

        self.fisk.write_register(Register.PF, 1 << Register.R0)
        self.fisk.write_register(Register.R0, 0)

        self.fisk.write_register(Register.PF, 0)
        self.fisk.write_register(Register.R0, 0)

    def test_fibonacci_raw(self):
        program = bytes([
            0b1001_0000, 0b0000_0000,  # 00:   movi     r0, 0
            0b1001_0001, 0b0000_0001,  # 02:   movi     r1, 1
            0b0110_0000, 0b0001_1000,  # 04:   add      r0, r1
            0b0110_0000, 0b0001_0111,  # 06:   swap     r0, r1
            0b1000_1011, 0b1111_1010,  # 08:   addi     pc, -4 (jmp 04)
        ])

        for offset, byte in enumerate(program):
            self.fisk.write_byte(0, offset, byte)

        for cycle in range(19):
            self.fisk.tick()

        self.assertEqual(self.fisk.read_register(0), 8)
        self.assertEqual(self.fisk.read_register(1), 13)

    def test_fibonacci_constructed(self):
        instructions = [
            Instruction.from_keywords(
                opcode=Opcode.MOVE_IMMEDIATE, register_a=Register.R0, imm8=0),
            Instruction.from_keywords(
                opcode=Opcode.MOVE_IMMEDIATE, register_a=Register.R1, imm8=1),
            Instruction.from_keywords(
                opcode=Opcode.ALU, operation=AluMode.ADD,
                register_a=Register.R0, register_b=Register.R1),
            Instruction.from_keywords(
                opcode=Opcode.ALU, operation=AluMode.SWAP,
                register_a=Register.R0, register_b=Register.R1),
            Instruction.from_keywords(
                opcode=Opcode.ADD_IMMEDIATE, register_a=Register.PC, imm8=-6)
        ]

        for i, instruction in enumerate(instructions):
            self.fisk.write_word(0, i*2, instruction.value)

        for cycle in range(19):
            self.fisk.tick()

        self.assertEqual(self.fisk.read_register(0), 8)
        self.assertEqual(self.fisk.read_register(1), 13)


class InstructionTestCase(unittest.TestCase):

    def setUp(self):
        self.instruction = Instruction(0b1011_1110_0011_0110)

    def test_reading_parts(self):
        self.assertEqual(self.instruction.opcode, 0b1011)

    def test_read_bit(self):
        self.assertEqual(self.instruction[0], 0)
        self.assertEqual(self.instruction[1], 1)
        self.assertEqual(self.instruction[2], 1)
        self.assertEqual(self.instruction[3], 0)
        self.assertEqual(self.instruction[14], 0)
        self.assertEqual(self.instruction[15], 1)

    def test_set_slice(self):
        self.instruction[15:12] = 0b1001
        self.assertEqual(self.instruction[15:12], 0b1001)

        self.instruction[15:0] = 0
        self.assertEqual(self.instruction.value, 0)

        self.instruction[15:0] = 0xFA5F
        self.assertEqual(self.instruction.value, 0xFA5F)

    def test_set_field(self):
        self.instruction.opcode = 0b1000
        self.assertEqual(self.instruction.opcode, 0b1000)

    def test_set_bit(self):
        self.instruction[0] = 0
        self.assertEqual(self.instruction[0], 0)
        self.instruction[0] = 1
        self.assertEqual(self.instruction[0], 1)
        self.instruction[15] = 0
        self.assertEqual(self.instruction[15], 0)
        self.instruction[15] = 1
        self.assertEqual(self.instruction[15], 1)

    def test_set_named_field(self):
        self.instruction.negate = 0
        self.assertEqual(self.instruction.negate, 0)
        self.instruction.negate = 1
        self.assertEqual(self.instruction.negate, 1)

    def test_from_keywords(self):
        i = Instruction.from_keywords(opcode=0b1111)
        self.assertEqual(i.opcode, 0b1111)


class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.word = Word()

    def test_set_value(self):
        self.word.value = 0xA5A5
        self.assertEqual(self.word.value, 0xA5A5)

    def test_get_bit(self):
        self.word.value = 0x0000
        self.assertEqual(self.word[15], 0)
        self.word.value = 0x8000
        self.assertEqual(self.word[15], 1)

    def test_set_bit(self):
        offset = 7

        self.word[offset] = 0
        self.assertEqual(self.word[offset], 0)
        self.word[offset] = 1
        self.assertEqual(self.word[offset], 1)

    def test_get_slice(self):
        self.word.value = 0xBABE

        self.assertEqual(self.word[4:11], 0xAB)
        self.assertEqual(self.word[11:4], 0xAB)
        self.assertEqual(self.word[15:0], 0xBABE)

    def test_set_slice(self):
        self.word.value = 0xFFFF
        self.word[0:7] = 0xA5

        self.assertEqual(self.word.value, 0xFFA5)


class UtilTestCase(unittest.TestCase):

    def test_sign_extend_positive(self):
        initial = 0b1001
        desired = 0b11111001

        self.assertEqual(sign_extend(initial, 4, 8), desired)

    def test_sign_extend_negative(self):
        initial = 0b01111111

        self.assertEqual(sign_extend(initial, 8, 16), initial)

    def test_bit_mask(self):
        self.assertEqual(bit_mask(0, 3), 0x0F)
        self.assertEqual(bit_mask(4, 7), 0xF0)
        self.assertEqual(bit_mask(8, 15), 0xFF00)

    def test_bit_mask_with_large_arguments(self):
        self.assertEqual(bit_mask(99, 100), 1 << 99 | 1 << 100)


if __name__ == '__main__':
    unittest.main()
