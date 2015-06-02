from opcode_factory import *

def test_int_arith32_immediate():
    #                 iiiiiiii      iii
    instr = 0b00000000010101010010000100011011
    name = 'add'
    rd = 1
    rn = 0
    imm = 0b01010101010
    assert int_arith32_immediate(name, rd, rn, imm) == instr


def test_int_arith32():
    instr = 0b00000000000010100100010000011111
    name = 'add'
    rd = 2
    rn = 1
    rm = 0
    assert int_arith32(name, rd, rn, rm) == instr
    instr = 0b00000000000010100100010000111111
    name = 'sub'
    rd = 2
    rn = 1
    rm = 0
    assert int_arith32(name, rd, rn, rm) == instr


def test_jr32():
    instr = 0b00000000000000100000000101001111
    rn = 0
    assert jr32(rn) == instr


def test_bcond32():
    instr = 0b00000000000000000000000000001000
    assert bcond32(0, 0) == instr
