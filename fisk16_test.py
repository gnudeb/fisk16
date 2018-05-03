import unittest

from fisk16.emulator import Fisk16, Register16
from fisk16.devices import ROMDevice


class Fisk16Tests(unittest.TestCase):
    def setUp(self):
        self.cpu = Fisk16()
        self.cpu.register(0).value = 0xbbaa
        self.cpu.register(1).value = 0xddcc

    def test_mov_r8_r8(self):
        # mov ah, al
        self.cpu.devices[0] = ROMDevice([0x04, 0x01, 0x00])
        self.cpu.tick()
        self.assertEqual(
            self.cpu.register(1, byte_sized=True).value,
            0xaa
        )

    def test_mov_r8_imm8(self):
        # mov al, imm8
        self.cpu.devices[0] = ROMDevice([0x04, 0x10, 0xef])
        self.cpu.tick()
        self.assertEqual(
            self.cpu.register(0, byte_sized=True).value,
            0xef
        )

    def test_mov_r16_r16(self):
        # mov b, a
        self.cpu.devices[0] = ROMDevice([0x04, 0x21, 0x00])
        self.cpu.tick()
        self.assertEqual(
            self.cpu.register(1).value,
            0xbbaa
        )

    def test_mov_r16_imm16(self):
        # mov a, 0xbeef
        self.cpu.devices[0] = ROMDevice([0x04, 0x30, 0xef, 0xbe])
        self.cpu.tick()
        self.assertEqual(
            self.cpu.register(0).value,
            0xbeef
        )


if __name__ == "__main__":
    unittest.main()