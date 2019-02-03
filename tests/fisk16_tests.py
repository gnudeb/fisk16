from fisk16.instruction import Instruction
from fisk16.types import Word

import unittest


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


if __name__ == '__main__':
    unittest.main()
