from collections import namedtuple

"""
reg - One of 16 possible register locations ranging from s0 through sF or specified as a literal

aaa - 10-bit address, specified either as a literal or a three-digit hexadecimal value ranging
      from 000 to 3FF or a labeled location

kk - 8-bit immediate constant, specified either as a literal or a two-digit hexadecimal value ranging
     from 00 to FF or specified as a literal

pp - 8-bit port address, specified either as a literal or a two-digit hexadecimal value ranging from 00 to FF
      or specified as a literal

ss - 6-bit scratchpad RAM address, specified either as a literal or a two-digit hexadecimal value
     ranging from 00 to 3F or specified as a literal
"""

""" INSTRUCTIONS """

ADD1 = namedtuple('ADD', ('reg', 'kk'))
ADD2 = namedtuple('ADD', ('reg', 'reg2'))

ADDC1 = namedtuple('ADDC', ('reg', 'kk'))
ADDC2 = namedtuple('ADDC', ('reg', 'reg2'))

AND1 = namedtuple('AND', ('reg', 'kk'))
AND2 = namedtuple('AND', ('reg', 'reg2'))

CALL = namedtuple('CALL', ('aaa',))
CALLX = namedtuple('CALL', ('flag', 'aaa'))

COMP1 = namedtuple('COMP', ('reg', 'kk'))
COMP2 = namedtuple('COMP', ('reg', 'reg2'))

DINT = namedtuple('DINT', ())
EINT = namedtuple('EINT', ())

FETCH1 = namedtuple('FETCH', ('reg', 'ss'))
FETCH2 = namedtuple('FETCH', ('reg', 'reg2'))

IN1 = namedtuple('IN', ('reg', 'reg2'))
IN2 = namedtuple('IN', ('reg', 'pp'))

JUMP = namedtuple('JUMP', ('aaa',))
JUMPX = namedtuple('JUMP', ('flag', 'aaa'))

LOAD1 = namedtuple('LOAD', ('reg', 'kk'))
LOAD2 = namedtuple('LOAD', ('reg', 'reg2'))

OR1 = namedtuple('OR', ('reg', 'kk'))
OR2 = namedtuple('OR', ('reg', 'reg2'))

OUT1 = namedtuple('OUT', ('reg', 'reg2'))
OUT2 = namedtuple('OUT', ('reg', 'pp'))

RET = namedtuple('RET', ())
RETX = namedtuple('RET', ('flag',))

RETI = namedtuple('RETI', ('ind',))

RL = namedtuple('RL', ('reg',))
SL0 = namedtuple('SL0', ('reg',))
SL1 = namedtuple('SL1', ('reg',))
SLA = namedtuple('SLA', ('reg',))
SLX = namedtuple('SLX', ('reg',))

RR = namedtuple('RR', ('reg',))
SR0 = namedtuple('SR0', ('reg',))
SR1 = namedtuple('SR1', ('reg',))
SRA = namedtuple('SRA', ('reg',))
SRX = namedtuple('SRX', ('reg',))

STORE1 = namedtuple('STORE', ('reg', 'ss'))
STORE2 = namedtuple('STORE', ('reg', 'reg2'))

SUB1 = namedtuple('SUB', ('reg', 'kk'))
SUB2 = namedtuple('SUB', ('reg', 'reg2'))

SUBC1 = namedtuple('SUBC', ('reg', 'kk'))
SUBC2 = namedtuple('SUBC', ('reg', 'reg2'))

TEST1 = namedtuple('TEST', ('reg', 'kk'))
TEST2 = namedtuple('TEST', ('reg', 'reg2'))

XOR1 = namedtuple('XOR', ('reg', 'kk'))
XOR2 = namedtuple('XOR', ('reg', 'reg2'))

""" DIRECTIVES """

ORG = namedtuple('ORG', ('addr',))

EQU1 = namedtuple('EQU', ('alias', 'reg'))
EQU2 = namedtuple('EQU', ('alias', 'kk'))

DSIN = namedtuple('DSIN', ('alias', 'pp'))
DSOUT = namedtuple('DSOUT', ('alias', 'pp'))
DSIO = namedtuple('DSIO', ('alias', 'pp'))

LABEL = namedtuple('LABEL', ('alias',))

MNEMONICS = {
    i.__name__: i for i in (ADD1, ADD2, ADDC1, ADDC2, AND1, AND2, CALL, CALLX, COMP1, COMP2, DINT, EINT, FETCH1, FETCH2,
                            IN1, IN2, JUMP, JUMPX, LOAD1, LOAD2, OR1, OR2, OUT1, OUT2, RET, RETX, RETI, RL, SL0, SL1,
                            SLA, SLX, RL, SR0, SR1, SRA, SRX, STORE1, STORE2, SUB1, SUB2, SUBC1, SUBC2, TEST1, TEST2,
                            XOR1, XOR2, ORG, EQU1, EQU2, DSIN, DSOUT, DSIO
                            )
}
