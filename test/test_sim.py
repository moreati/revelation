from epiphany.test.sim import MockEpiphany
from epiphany.test.machine import StateChecker

import opcode_factory

def test_single_inst_add32():
    instructions = [opcode_factory.add32_immediate(rd=1, rn=0, imm=0b01010101010),
                    opcode_factory.bkpt16()]
    epiphany = MockEpiphany()
    epiphany.init_test_state(instructions)
    epiphany.state.rf[0] = 0b01010101010
    epiphany.run()
    expected_state = StateChecker(AZ=0, pc=6, rf1=(0b01010101010 * 2))
    expected_state.check(epiphany.state)


def test_single_inst_sub32():
    from pydgin.utils import trim_32
    instructions = [opcode_factory.sub32_immediate(rd=1, rn=0, imm=0b01010101010),
                    opcode_factory.bkpt16()]
    epiphany = MockEpiphany()
    epiphany.init_test_state(instructions)
    epiphany.state.rf[0] = 5
    epiphany.run()
    expected_state = StateChecker(AZ=0, AN=1, AC=1, pc=6, rf1=trim_32(5 - 0b01010101010))
    expected_state.check(epiphany.state)


def test_add32_sub32():
    from pydgin.utils import trim_32
    instructions = [opcode_factory.add32_immediate(rd=1,rn=0, imm=0b01010101010),
    # TODO: Add new instruction to move the result of instruction 1
    # TODO: to rf[0] before instruction 2 is executed.
                    opcode_factory.sub32_immediate(rd=1, rn=0, imm=0b01010101010),
                    opcode_factory.bkpt16(),
                    ]
    epiphany = MockEpiphany()
    epiphany.init_test_state(instructions)
    epiphany.state.rf[0] = 0
    epiphany.run()
    expected_state = StateChecker(AZ=0, AN=1, AC=1, pc=10, rf1=trim_32(0 - 0b01010101010))
    expected_state.check(epiphany.state)


def test_bcond32():
    instructions = [opcode_factory.sub32_immediate(rd=1, rn=0, imm=0b00000000101),
                    opcode_factory.bcond32(condition=0b0000, imm=0b000000000000000000000100),
                    opcode_factory.add32_immediate(rd=1, rn=0, imm=0b01010101010),
                    opcode_factory.bkpt16(),
                    ]
    epiphany = MockEpiphany()
    epiphany.init_test_state(instructions)
    epiphany.state.rf[0] = 5
    epiphany.run()
    expected_state = StateChecker(pc=14, rf1=0)
    expected_state.check(epiphany.state)
    epiphany.init_test_state(instructions)
    epiphany.state.rf[0] = 8
    epiphany.run()
    expected_state = StateChecker(pc=14, rf1=(8 + 0b01010101010))
    expected_state.check(epiphany.state)


def test_add32_nop16_sub32():
    from pydgin.utils import trim_32
    instructions = [opcode_factory.add32_immediate(rd=1, rn=0, imm=0b01010101010),
                    opcode_factory.nop16(),
                    opcode_factory.sub32_immediate(rd=1, rn=0, imm=0b01010101010),
                    opcode_factory.bkpt16(),
                    ]
    epiphany = MockEpiphany()
    epiphany.init_test_state(instructions)
    epiphany.state.rf[0] = 0
    epiphany.run()
    expected_state = StateChecker(pc=14, AC=1, AN=1, AZ=0, rf1=trim_32(0 - 0b01010101010))
    expected_state.check(epiphany.state)
