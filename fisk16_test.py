import unittest

from fisk16.emulator import Fisk16


class Fisk16InstructionsTests(unittest.TestCase):

    def setUp(self):
        self.cpu = Fisk16()

    def test_mov_r16_r16(self):
        self.cpu.ram.write(0, 0x0010, 2)    # mov r1, r0
        self.cpu.register_ram.write('r0', 0xbeef)

        self.cpu.tick()
        self.assertEqual(self.cpu.register_ram.read('r1'), 0xbeef)

    def test_r16_ind(self):
        self.cpu.ram.write(0, 0x0110, 2)    # mov r1, [r0]
        self.cpu.ram.write(8, 0xbeef, 2)
        self.cpu.register_ram.write('r0', 8)  # r0 = 8

        self.cpu.tick()
        self.assertEqual(self.cpu.register_ram.read('r1'), 0xbeef)

    def test_ind_r16(self):
        self.cpu.ram.write(0, 0x0210, 2)    # mov [r1], r0
        self.cpu.register_ram.write('r0', 0xbeef)
        self.cpu.register_ram.write('r1', 8)

        self.cpu.tick()
        self.assertEqual(self.cpu.ram.read(8, 2), 0xbeef)

    def test_r8_r8(self):
        self.cpu.ram.write(0, 0x0310, 2)    # mov r0h, r0l
        self.cpu.register_ram.write('r0l', 0xa5)

        self.cpu.tick()
        self.assertEqual(self.cpu.register_ram.read('r0h'), 0xa5)

    def test_r8_ind(self):
        self.cpu.ram.write(0, 0x0401, 2)      # mov r0l, [r1]
        self.cpu.register_ram.write('r1', 8)  # r1 = 8
        self.cpu.ram.write(8, 0xa5)

        self.cpu.tick()
        self.assertEqual(self.cpu.register_ram.read('r0l'), 0xa5)

    def test_ind_r8(self):
        self.cpu.ram.write(0, 0x0510, 2)      # mov [r1], r0l
        self.cpu.register_ram.write('r1', 8)
        self.cpu.register_ram.write('r0l', 0xa5)

        self.cpu.tick()
        self.assertEqual(self.cpu.ram.read(8), 0xa5)

    def test_r16_imm16(self):
        self.cpu.ram.write(0, 0x0600beef, 4)  # mov r0, 0xbeef

        self.cpu.tick()
        self.assertEqual(self.cpu.register_ram.read('r0'), 0xbeef)

    def test_r8_imm8(self):
        self.cpu.ram.write(0, 0x0700a5, 3)  # mov r0l, 0xa5

        self.cpu.tick()
        self.assertEqual(self.cpu.register_ram.read('r0l'), 0xa5)


if __name__ == "__main__":
    unittest.main()
