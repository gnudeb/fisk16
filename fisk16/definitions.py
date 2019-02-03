from enum import IntEnum


class Opcode(IntEnum):
    PUSH = 0
    POP = 1
    STORE = 2
    LOAD = 3
    BOOLEAN = 4
    JUMP_IF_BIT = 5
    ALU = 6
    CALL = 7
    ADD_IMMEDIATE = 8
    MOVE_IMMEDIATE = 9


class AluMode(IntEnum):
    MOV = 0
    OR = 1


class Register(IntEnum):
    R0 = 0
    SP = 11
    PC = 12
