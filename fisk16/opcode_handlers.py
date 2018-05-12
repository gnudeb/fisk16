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
}
