from . import instructions as i


handlers = {
    0x00: i.mov_r16_r16,
    0x01: i.mov_r16_ind,
    0x02: i.mov_ind_r16,
    0x03: i.mov_r8_r8,
    0x04: i.mov_r8_ind,
    0x05: i.mov_ind_r8,
    0x06: i.mov_r16_imm16,
    0x07: i.mov_r8_imm8,
    0x08: i.or_r16_r16,
    0x09: i.or_r8_r8,
    0x0a: i.or_r16_imm16,
    0x0b: i.or_r8_imm8,
    0x0c: i.and_r16_r16,
    0x0d: i.and_r8_r8,
    0x0e: i.and_r16_imm16,
    0x0f: i.and_r8_imm8,
    0x10: i.add_r16_r16,
    0x11: i.add_r16_imm16,
}
