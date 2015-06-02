from opcode_factory import int_arith32_immediate, int_arith32

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
