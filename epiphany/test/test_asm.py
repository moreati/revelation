from epiphany.sim import Epiphany
from epiphany.utils import float2bits
from epiphany.test.machine import StateChecker

import os.path
import pytest

elf_dir = os.path.join('epiphany', 'test', 'asm')

@pytest.mark.parametrize("elf,expected",
       [('add.elf', StateChecker(rf1=110, rf2=7, rf3=105)),
        ('and.elf', StateChecker(rf0=0, rf1=1, rf2=1, rf3=0, rf4=0, rf5=0)),
        ('asr.elf', StateChecker(rf0=1, rf1=5, rf2=0, rf3=0)),
        ('bcond.elf', StateChecker(rf0=0, rf1=110)),
        ('bitr.elf', StateChecker(rf0=0x84c2a6e1)),
        ('bl.elf', StateChecker(rf0=15, rf1=0, rf2=15)),
        pytest.mark.xfail(('dma_transfer.elf', StateChecker())),
        ('eor.elf', StateChecker(rf0=5, rf1=7, rf2=2)),
        ('fix.elf', StateChecker(rf0=5)),
        ('gid.elf', StateChecker(rfSTATUS=0b10)),
        ('gie.elf', StateChecker(rfSTATUS=0b00)),
        pytest.mark.xfail(('hardware_loop.elf',
         StateChecker(rf0=100, rf1=116, rf2=100, rf3=100,
                      rf4=100, rf5=100, rf6=100, rf7=100, rf8=100, rfSTATUS=0b00))),
        ('jalr.elf', StateChecker(rf3=100, rfLR=0x236)),
        ('jr.elf', StateChecker(rf0=3, rf1=1, rf2=2)),
        ('low_high.elf', StateChecker(rf3=0xFFFFFFFF)),
        ('lsl.elf', StateChecker(rf0=5, rf1=7, rf2=640, rf3=640)),
        ('lsr.elf', StateChecker(rf0=3, rf1=1, rf2=1, rf3=1)),
        ('mov_cond.elf', StateChecker(rf0=0, rf1=15, rf2=15, rf3=15)),
        pytest.mark.xfail(('movfs.elf', StateChecker(rf0=7, rf63=7, rfIRET=7))),
        ('mov_imm.elf', StateChecker(rf0=25)),
        ('movt.elf', StateChecker(rf0=2415919104)),
        ('movts.elf', StateChecker(rf0=7, rfIRET=7)),  # FIXME
        ('nop.elf', StateChecker(pc=564)),
        ('orr.elf', StateChecker(rf0=5, rf1=7, rf2=7)),
        pytest.mark.xfail(('rti.elf', StateChecker())), # FIXME
        ('rts.elf', StateChecker(rf1=100, rf2=200, rf3=300, rfLR=562)),
        ('sub.elf', StateChecker(rf0=100, rf1=20, rf2=80, rf3=80)),
        pytest.mark.xfail(('trap.elf', StateChecker())),
       ])
def test_elf(elf, expected):
    """Test ELF files that deal in unsigned integers (rather than floats).
    """
    elf_filename = os.path.join(elf_dir, elf)
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.max_insts = 10000
        epiphany.run()
        expected.check(epiphany.state)


@pytest.mark.parametrize("elf,expected",
                         [('fabs.elf', StateChecker(rf0=float2bits(5.0),
                                                    rf1=float2bits(0.0),
                                                    rf2=float2bits(-5.0),
                                                    rf3=float2bits(5.0),
                                                    rf4=float2bits(0.0),
                                                    rf5=float2bits(5.0),
                                                    )),
                          ('float.elf', StateChecker(rf1=float2bits(25.0))),
                          ('fadd.elf', StateChecker(rf0=float2bits(15.0),
                                                    rf1=float2bits(5.0),
                                                    rf2=float2bits(5.0),
                                                    rf3=float2bits(10.0),
                                                    rf4=float2bits(0.0))),
                          ('fsub.elf', StateChecker(rf0=float2bits(0.0),
                                                    rf1=float2bits(2.0),
                                                    rf2=float2bits(5.0),
                                                    rf3=float2bits(5.0),
                                                    rf4=float2bits(3.0),
                                                    rf5=float2bits(-3.0))),
                          ('fmul.elf', StateChecker(rf0=float2bits(0.0),
                                                    rf1=float2bits(2.0),
                                                    rf2=float2bits(5.0),
                                                    rf3=float2bits(0.0),
                                                    rf4=float2bits(10.0))),
                          ('fmadd.elf', StateChecker(rf0=float2bits(0.0),
                                                     rf1=float2bits(2.0),
                                                     rf2=float2bits(5.0),
                                                     rf3=float2bits(17.0),
                                                     rf4=float2bits(7.0))),
                          ('fmsub.elf', StateChecker(rf0=float2bits(0.0),
                                                     rf1=float2bits(2.0),
                                                     rf2=float2bits(5.0),
                                                     rf3=float2bits(-3.0),
                                                     rf4=float2bits(7.0))),
                          ('iadd.elf', StateChecker(rf0=float2bits(15.0),
                                                    rf1=float2bits(5.0),
                                                    rf2=float2bits(5.0),
                                                    rf3=float2bits(10.0),
                                                    rf4=float2bits(0.0))),
                          ('isub.elf', StateChecker(rf0=float2bits(0.0),
                                                    rf1=float2bits(2.0),
                                                    rf2=float2bits(5.0),
                                                    rf3=float2bits(5.0),
                                                    rf4=float2bits(3.0),
                                                    rf5=float2bits(-3.0))),
                          ('imul.elf', StateChecker(rf0=float2bits(0.0),
                                                    rf1=float2bits(2.0),
                                                    rf2=float2bits(5.0),
                                                    rf3=float2bits(0.0),
                                                    rf4=float2bits(10.0))),
                          ('imadd.elf', StateChecker(rf0=float2bits(0.0),
                                                     rf1=float2bits(2.0),
                                                     rf2=float2bits(5.0),
                                                     rf3=float2bits(17.0),
                                                     rf4=float2bits(7.0))),
                          ('imsub.elf', StateChecker(rf0=float2bits(0.0),
                                                     rf1=float2bits(2.0),
                                                     rf2=float2bits(5.0),
                                                     rf3=float2bits(-3.0),
                                                     rf4=float2bits(7.0))),
                         ])
def test_fp_elf(elf, expected):
    """Check that floating point instructions operate correctly.
    These ELF files are tested separately using the fp_check method.
    This means that test failures will be reported so that the contents of
    registers are printed as floats, rather than as unsigned integers.
    """
    elf_filename = os.path.join(elf_dir, elf)
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.max_insts = 10000
        epiphany.run()
        expected.fp_check(epiphany.state)


@pytest.mark.parametrize("elf,expected",
       [('ldr_disp.elf',    StateChecker(rf0=0xFFFFFFFF, rf1=0x00100000)),
        ('ldr_disp_pm.elf', StateChecker(rf0=0xFFFFFFFF, rf1=0x00100004)),
        ('ldr_index.elf',   StateChecker(rf0=0xFFFFFFFF, rf1=0x00100004, rf2=0)),
        ('ldr_pm.elf',      StateChecker(rf0=0xFFFFFFFF, rf1=0x00100004,
                                         rf2=0x80002)),
       ])
def test_load(elf, expected):
    """Test ELF files that load values from memory into a register.
    """
    elf_filename = os.path.join(elf_dir, elf)
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.state.mem.write(0x00100004, 4, 0xFFFFFFFF)
        epiphany.max_insts = 10000
        epiphany.run()
        expected.check(epiphany.state)


@pytest.mark.parametrize("elf,expected",
       [('str_disp.elf', StateChecker(rf0=0xFFFFFFFF, rf1=0x00100000)),
        ('str_disp_pm.elf', StateChecker(rf0=0xFFFFFFFF, rf1=0x00100004)),
        ('str_index.elf', StateChecker(rf0=0xFFFFFFFF, rf1=0x00100004, rf2=0)),
        ('str_pm.elf', StateChecker(rf0=0xFFFFFFFF, rf1=0x00100004, rf2=4)),
       ])
def test_store(elf, expected):
    """Test ELF files that transfer data from registers to memory.
    """
    elf_filename = os.path.join(elf_dir, elf)
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.max_insts = 10000
        epiphany.run()
        expected.check(epiphany.state, memory=[(0x00100004, 4, 0xFFFFFFFF)])


def test_testset32():
    elf_filename = os.path.join(elf_dir, 'testset.elf')
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        if elf == 'movts.elf': print 'MOVTS'
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.state.mem.write(0x100004, 4, 0x0)
        epiphany.max_insts = 100000
        epiphany.run()
        expected = StateChecker(AZ=1, rf0=0, rf1=0x100000, rf2=0x4)
        expected.check(epiphany.state, memory=[(0x100004, 4, 0xFFFF)])


def test_testset32_fail():
    """Check that the testset32 instruction fails if the memory address it
    is given is too low..
    """
    elf_filename = os.path.join(elf_dir, 'testset_fail.elf')
    expected_text = """testset32 has failed to write to address %s.
The absolute address used for the test and set instruction must be located
within the on-chip local memory and must be greater than 0x00100000 (2^20).
""" % str(hex(0x4))
    with pytest.raises(ValueError) as expected_exn:
        epiphany = Epiphany()
        with open(elf_filename, 'rb') as elf:
            epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
            epiphany.max_insts = 100000
            epiphany.run()
    assert expected_text == expected_exn.value.message


def test_execute_idle16(capsys):
    """Check that the idle16 prints out the correct warning on STDOUT.
    """
    elf_filename = os.path.join(elf_dir, 'idle.elf')
    epiphany = Epiphany()
    with open(elf_filename, 'rb') as elf:
        epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
        epiphany.state.rfSTATUS = 1
        epiphany.max_insts = 10000
        epiphany.run()
        out, err = capsys.readouterr()
        expected_state = StateChecker(rfSTATUS=0)
        expected_text = ('IDLE16 does not wait in this simulator. ' +
                         'Moving to next instruction.')
        expected_state.check(epiphany.state)
        assert expected_text in out
        assert err == ''
        assert not epiphany.state.running  # Set by bkpt16 instruction.


def test_unimpl():
    """Check that the unimpl instruction throws a NotImplementedError.
    """
    elf_filename = os.path.join(elf_dir, 'unimpl.elf')
    with pytest.raises(NotImplementedError):
        epiphany = Epiphany()
        with open(elf_filename, 'rb') as elf:
            epiphany.init_state(elf, elf_filename, '', [], False, is_test=True)
            epiphany.run()
