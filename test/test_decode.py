from epiphany.isa import decode
from epiphany.instruction import Instruction

import opcode_factory

import pytest

@pytest.mark.parametrize("name,instr",
                         [("add32",      opcode_factory.int_arith32("add", 0, 0, 0)),
                          ("add16",      opcode_factory.int_arith16("add", 0, 0, 0)),
                          ("add32",      opcode_factory.int_arith32("add", 1, 1, 1)),
                          ("add16",      opcode_factory.int_arith16("add", 1, 1, 1)),
                          ("sub32",      opcode_factory.int_arith32("sub", 0, 0, 0)),
                          ("sub16",      opcode_factory.int_arith16("sub", 0, 0, 0)),
                          ("sub32",      opcode_factory.int_arith32("sub", 1, 1, 1)),
                          ("sub16",      opcode_factory.int_arith16("sub", 1, 1, 1)),
                          ("add32",      opcode_factory.int_arith32_immediate("add", 1, 0, 0b01010101010)),
                          ("add16",      opcode_factory.int_arith16_immediate("add", 1, 0, 0b0101)),
                          ("sub32",      opcode_factory.int_arith32_immediate("sub", 1, 0, 0b01010101010)),
                          ("sub16",      opcode_factory.int_arith16_immediate("sub", 1, 0, 0b0101)),
                          ("and32",      opcode_factory.int_arith32("and", 1, 1, 1)),
                          ("and16",      opcode_factory.int_arith16("and", 1, 1, 1)),
                          ("orr32",      opcode_factory.int_arith32("orr", 1, 1, 1)),
                          ("orr16",      opcode_factory.int_arith16("orr", 1, 1, 1)),
                          ("eor32",      opcode_factory.int_arith32("eor", 1, 1, 1)),
                          ("eor16",      opcode_factory.int_arith16("eor", 1, 1, 1)),
                          ("asr32",      opcode_factory.int_arith32("asr", 1, 1, 1)),
                          ("asr16",      opcode_factory.int_arith16("asr", 1, 1, 1)),
                          ("lsr32",      opcode_factory.int_arith32("lsr", 1, 1, 1)),
                          ("lsr16",      opcode_factory.int_arith16("lsr", 1, 1, 1)),
                          ("lsl32",      opcode_factory.int_arith32("lsl", 1, 1, 1)),
                          ("lsl16",      opcode_factory.int_arith16("lsl", 1, 1, 1)),
                          ("lsrimm16",   opcode_factory.bit16_immediate("lsr", 1, 1, 1)),
                          ("lslimm16",   opcode_factory.bit16_immediate("lsl", 1, 1, 1)),
                          ("asrimm16",   opcode_factory.bit16_immediate("asr", 1, 1, 1)),
                          ("bitrimm16",  opcode_factory.bit16_immediate("bitr", 1, 1, 1)),
                          ("lsrimm32",   opcode_factory.bit32_immediate("lsr", 1, 1, 1)),
                          ("lslimm32",   opcode_factory.bit32_immediate("lsl", 1, 1, 1)),
                          ("asrimm32",   opcode_factory.bit32_immediate("asr", 1, 1, 1)),
                          ("bitrimm32",  opcode_factory.bit32_immediate("bitr", 1, 1, 1)),
                          ("jr32",       opcode_factory.jr32(0)),
                          ("jr16",       opcode_factory.jr16(0)),
                          ("bcond32",    opcode_factory.bcond32(0b1111, 0)),
                          ("bcond16",    opcode_factory.bcond16(0b1111, 0)),
                          ("ldstrpmd32", opcode_factory.ldstrpmd32(1, 0, 1, 0b1010101010, 0b11, 1)),
                          ("movcond32",  opcode_factory.movcond32(0b0000, 0, 0)),
                          ("movcond16",  opcode_factory.movcond16(0b0000, 0, 0)),
                          ("movtimm32",  opcode_factory.movtimm32(0b1111, 0)),
                          ("movimm32",   opcode_factory.movimm32(0b1111, 0)),
                          ("movimm16",   opcode_factory.movimm16(0b1111, 0)),
                          ("gie16",      opcode_factory.gie16()),
                          ("gid16",      opcode_factory.gid16()),
                          ("nop16",      opcode_factory.nop16()),
                          ("idle16",     opcode_factory.idle16()),
                          ("bkpt16",     opcode_factory.bkpt16()),
                          ("mbkpt16",    opcode_factory.mbkpt16()),
                          ("sync16",     opcode_factory.sync16()),
                          ("rti16",      opcode_factory.rti16()),
                          ("wand16",     opcode_factory.wand16()),
                          ("trap16",     opcode_factory.trap16(0b111111)),
                          ("unimpl16",   opcode_factory.unimpl16()),
                         ])
def test_decode(name, instr):
    decoded_name, _ = decode(instr)
    assert decoded_name == name


def test_bit32_imm():
    instr = Instruction(opcode_factory.bit32_immediate("bitr", 0b110110, 0b101101, 0b11111),
                        None)
    assert instr.imm5 == 0b11111
    assert instr.rd == 0b110110
    assert instr.rn == 0b101101
    instr = Instruction(opcode_factory.bit32_immediate("lsr", 0, 0, 0b01011),
                        None)
    assert instr.imm5 == 0b01011


def test_bit16_imm():
    instr = Instruction(opcode_factory.bit16_immediate("bitr", 0b110, 0b101, 0b11111),
                        None)
    assert instr.imm5 == 0b11111
    assert instr.rd == 0b110
    assert instr.rn == 0b101
    instr = Instruction(opcode_factory.bit16_immediate("lsr", 0, 0, 0b01011),
                        None)
    assert instr.imm5 == 0b01011


def test_decode_add32():
    instr = opcode_factory.int_arith32("add", 0, 0, 0)
    name, _ = decode(instr)
    assert name == "add32"
    instr = opcode_factory.int_arith32("add", 1, 1, 1)
    name, _ = decode(instr)
    assert name == "add32"


def test_decode_sub32():
    instr = opcode_factory.int_arith32("sub", 0, 0, 0)
    name, _ = decode(instr)
    assert name == "sub32"
    instr = opcode_factory.int_arith32("sub", 1, 1, 1)
    name, _ = decode(instr)
    assert name == "sub32"


def test_decode_ldstrpmd32():
    instr = opcode_factory.ldstrpmd32(1, 0, 1, 0b1010101010, 0b11, 1)
    name, executefn = decode(instr)
    assert Instruction(instr, "").sub_bit24 == 1
    assert Instruction(instr, "").bit4 == 1
    assert Instruction(instr, "").bits_5_6 == 0b11


def test_decode_add32_immediate_argument():
    instr = Instruction(opcode_factory.int_arith32_immediate("add", 1, 0, 0b01010101010), "")
    assert instr.rd == 1
    assert instr.rn == 0
    assert instr.imm == 0b01010101010
