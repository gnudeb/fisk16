Fisk16 specification
====================
Version 0.1



Summary
-------

* 16-bit address space (64K)
* 16 slots for memory mapped devices, 4K each
* 16 registers (x, y, a, b, c, d, e, f, g, h, i, j, k, pc, sp, fr)
* First 8 registers are byte-addressable (xl, xh, al, ah, ..., fl, fh)
* pc - program counter
* sp - stack pointer
* fr - flag register


Instructions
------------

```
0x00        - nop
0x01        - <reserved>
0x02..0x07  - mov byte
0x08
0x09
0x0a..0x0f  - mov word
```