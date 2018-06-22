from .instructions import\
    (r16_r16, r16_ind, ind_r16, r8_r8, r8_ind, ind_r8, r16_imm16, r8_imm8,
     mov,)

instruction_set = {
    0x00: (mov, r16_r16),
    0x01: (mov, r16_ind),
    0x02: (mov, ind_r16),
    0x03: (mov, r8_r8),
    0x04: (mov, r8_ind),
    0x05: (mov, ind_r8),
    0x06: (mov, r16_imm16),
    0x07: (mov, r8_imm8),
}
