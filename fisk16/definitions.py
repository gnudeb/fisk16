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


class BoolMode(IntEnum):
    SET_IF_EQUAL = 0
    SET_IF_NEGATIVE = 1
    SET_IF_LESS_THAN = 2
    SET_IF_LESS_UNSIGNED = 3
    SET_IF_ZERO = 4


class AluMode(IntEnum):
    MOV = 0
    OR = 1
    SWAP = 7


class Register(IntEnum):
    R0 = 0
    SP = 11
    PC = 12
    PF = 15
