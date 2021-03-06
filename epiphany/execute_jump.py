import epiphany.isa
from pydgin.utils import trim_32

#-----------------------------------------------------------------------
# jr32 and jr16 - jump.
# jalr32 and jalr16 - register and link jump.
#-----------------------------------------------------------------------
def make_jr_executor(is16bit, save_lr):
    def execute_jr(s, inst):
        """
        LR = PC + 2 (16 bit) 4 (32 bit)    JALR only.
        PC = RN;
        """
        if is16bit:
            inst.bits &= 0xffff
        if save_lr:
            s.rf[epiphany.isa.reg_map['LR']] = trim_32(s.pc + (2 if is16bit else 4))
        s.pc = s.rf[inst.rn]
    return execute_jr
