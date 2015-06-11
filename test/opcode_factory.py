def make_zero_operand_factory(opcode):
    def factory():
        return opcode
    return factory

gie16    = make_zero_operand_factory(0b00000000000000000000000110010010)
gid16    = make_zero_operand_factory(0b00000000000000000000001110010010)
nop16    = make_zero_operand_factory(0b0000000000000000000000110100010)
idle16   = make_zero_operand_factory(0b0000000000000000000000110110010)
bkpt16   = make_zero_operand_factory(0b00000000000000000000000111000010)
mbkpt16  = make_zero_operand_factory(0b00000000000000000000001111000010)
sync16   = make_zero_operand_factory(0b00000000000000000000000111110010)
rti16    = make_zero_operand_factory(0b00000000000000000000000111010010)
wand16   = make_zero_operand_factory(0b00000000000000000000000110000010)
unimpl16 = make_zero_operand_factory(0b00000000000011110000000000001111)


def trap16(trap):
    return 0b1111100010 | (trap << 10)


def int_arith32_immediate(name, rd, rn, imm):
    if name == 'add':
        opcode = 0b0011011
    elif name == 'sub':
        opcode = 0b0111011
    else:
        raise NotImplementedError()
    return (opcode | ((imm & 7) << 7) | ((rn & 7) << 10) |
            ((rd & 7) << 13) | ((imm & (0xFF << 3)) << 13) |
            ((rn & 56) << 23) | ((rd & 56) << 26))


def int_arith32(name, rd, rn, rm):
    bits_16_20 = 0b1010
    if name == 'add':
        opcode = 0b0011111
    elif name == 'sub':
        opcode = 0b0111111
    elif name == 'and':
        opcode = 0b1011111
    elif name == 'orr':
        opcode = 0b1111111
    elif name == 'eor':
        opcode = 0b0001111
    elif name == 'asr':
        opcode = 0b1101111
    elif name == 'lsr':
        opcode = 0b1001111
    elif name == 'lsl':
        opcode = 0b0101111
    else:
        raise NotImplementedError()
    return (opcode | ((rm & 7) << 7) | ((rn & 7) << 10) |
            ((rd & 7) << 13) | (bits_16_20 << 16) |
            ((rm & 56) << 20) | ((rn & 56) << 23) | ((rd & 56) << 26))


def bit32_immediate(name, rd, rn, imm):
    if name == 'lsr':
        opcode = 0b01111
        bits_16_20 = 0b0110
    elif name == 'lsl':
        opcode = 0b11111
        bits_16_20 = 0b0110
    elif name == 'asr':
        opcode = 0b01111
        bits_16_20 = 0b1110
    elif name == 'bitr':
        opcode = 0b11111
        bits_16_20 = 0b1110
    else:
        raise NotImplementedError()
    return (opcode | (imm << 5) | ((rn & 7) << 10) | ((rd & 7) << 13) |
            (bits_16_20 << 16) | ((rn & 56) << 23) | ((rd & 56) << 26))


def bit16_immediate(name, rd, rn, imm):
    if name == 'lsr':
        opcode = 0b00110
    elif name == 'lsl':
        opcode = 0b10110
    elif name == 'asr':
        opcode = 0b01110
    elif name == 'bitr':  # No immediate on pp 81 of reference manual.
        opcode = 0b11110
    else:
        raise NotImplementedError()
    return (opcode | (imm << 5) | (rn  << 10) | (rd << 13))


def int_arith16(name, rd, rn, rm):
    assert rd <= 0b111
    assert rn <= 0b111
    assert rm <= 0b111
    if name == 'add':
        opcode = 0b0011010
    elif name == 'sub':
        opcode = 0b0111010
    elif name == 'and':
        opcode = 0b1011010
    elif name == 'orr':
        opcode = 0b1111010
    elif name == 'eor':
        opcode = 0b0001010
    elif name == 'asr':
        opcode = 0b1101010
    elif name == 'lsr':
        opcode = 0b1001010
    elif name == 'lsl':
        opcode = 0b0101010
    else:
        raise NotImplementedError()
    return (opcode | ((rm & 7) << 7) | ((rn & 7) << 10) | ((rd & 7) << 13))


def int_arith16_immediate(name, rd, rn, imm):
    if name == 'add':
        opcode = 0b0010011
    elif name == 'sub':
        opcode = 0b0110011
    else:
        raise NotImplementedError()
    return (opcode | ((imm & 7) << 7) | ((rn & 7) << 10) | ((rd & 7) << 13))


def jr32(rn):
    opcode = 0b0101001111
    bits_16_20 = 0b0010
    return (opcode | ((rn & 7)) << 7) | (bits_16_20 << 16) | ((rn & 56) << 23)


def jr16(rn):
    opcode = 0b0101000010
    return (opcode | ((rn & 7) << 7))


def bcond_factory(is16bit):
    def bcond(cond, imm):
        opcode = 0b0000 if is16bit else 0b1000
        return (opcode | (cond << 4) | (imm << 8))
    return bcond
bcond32 = bcond_factory(False)
bcond16 = bcond_factory(True)


def movcond32(cond, rd, rn):
    opcode = 0b1111
    bits_16_20 = 0b0010
    return (opcode | (cond << 4) | ((rn & 7) << 10) |
            ((rd & 7) << 13) | (bits_16_20 << 16) |
            ((rn & 56) << 23) | ((rd & 56) << 26))


def movcond16(cond, rd, rn):
    opcode = 0b0010
    bits_9_10 = 0b00
    return (opcode | (cond << 4) | (bits_9_10 << 8) | (rn << 10) | (rd << 13))


def make_movimm32(is_t):
    def mov32_instruction(rd, imm):
        opcode = 0b01011
        bit28 = 1 if is_t else 0
        instruction = (opcode | ((imm & 255) << 5) | ((rd & 7) << 13) |
                       ((imm & 65280) << 12) | (bit28 << 28) | ((rd & 56) << 26))
        return instruction
    return mov32_instruction

movimm32  = make_movimm32(False)
movtimm32 = make_movimm32(True)


def movimm16(rd, imm):
    opcode = 0b00011
    return (opcode | (imm << 5) | (rd << 13))


def ldstrpmd32(rd, rn, sub, imm, bb, s):
    # Data size
    # 00=byte, 01=half-word, 10=word, 11=double-word
    opcode = 0b1100
    bit25 = 1
    return (opcode | (s << 4) | (bb << 5) | ((imm & 7) << 7) |
            ((rn & 7) << 10) | ((rd & 7) << 13) |
            ((imm & (0xFF << 3)) << 13) | (sub << 24) | (bit25 << 25) |
            ((rn & 56) << 23) | ((rd & 56) << 26))
