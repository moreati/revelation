#include "epiphany-macros.h"
SET_UP
    strb r31, [r2, r1] ;stores byte to addr in r2
    str r0, [r2, r1] ;stores word to addr in r2
TEAR_DOWN