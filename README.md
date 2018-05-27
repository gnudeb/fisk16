Fisk16 instruction set manual
=============================


Opcode table
------------

| Opcode | Mnemonic + operands |
|:------:| ------------------- |
|  0x00  | mov  r16,    r16    |
|  0x01  | mov  r16,    [r16]  |
|  0x02  | mov  [r16],  r16    |
|  0x03  | mov  r8,     r8     |
|  0x04  | mov  r8,     [r16]  |
|  0x05  | mov  [r16],  r8     |
|  0x06  | mov  r16,    imm16  |
|  0x07  | mov  r8,     imm8   |
|  0x08  | or   r16,    r16    |
|  0x09  | or   r8,     r8     |
|  0x0a  | or   r16,    imm16  |
|  0x0b  | or   r8,     imm8   |
|  0x0c  | and  r16,    r16    |
|  0x0d  | and  r8,     r8     |
|  0x0e  | and  r16,    imm16  |
|  0x0f  | and  r8,     imm8   |
|  0x10  | xor  r16,    r16    |
|  0x11  | xor  r8,     r8     |
|  0x12  | xor  r16,    imm16  |
|  0x13  | xor  r8,     imm8   |
|  0x14  | add  r16,    r16    |
|  0x15  | add  r8,     r8     |
|  0x16  | add  r16,    imm16  |
|  0x17  | add  r8,     imm8   |
|  0x18  | addc r16,    r16    |
|  0x19  | addc r8,     r8     |
|  0x1a  | addc r16,    imm16  |
|  0x1b  | addc r8,     imm8   |
|  0x1c  | sub  r16,    r16    |
|  0x1d  | sub  r8,     r8     |
|  0x1e  | sub  r16,    imm16  |
|  0x1f  | sub  r8,     imm8   |
|  0x20  | subc r16,    r16    |
|  0x21  | subc r8,     r8     |
|  0x22  | subc r16,    imm16  |
|  0x23  | subc r8,     imm8   |
|  0x24  | xch  r16,    r16    |
|  0x25  | xch  r8,     r8     |
|  0x26  |      RESERVED       |
|  0x27  |      RESERVED       |
|  0x28  | cmp  r16,    r16    |
|  0x29  | cmp  r8,     r8     |
|  0x2a  | cmp  r16,    imm16  |
|  0x2b  | cmp  r8,     imm8   |
