from collections import namedtuple

""" INSTRUCTIONS """

ADD = namedtuple('ADD', ('reg', 'reg_or_val'))

ADDC = namedtuple('ADDC', ('reg', 'reg_or_val'))

AND = namedtuple('AND', ('reg', 'reg_or_val'))

CALL = namedtuple('CALL', ('label_or_ind', 'label'))

COMP = namedtuple('COMP', ('reg', 'reg_or_val'))

DINT = namedtuple('DINT', ())
EINT = namedtuple('EINT', ())

FETCH = namedtuple('FETCH', ('reg', 'reg_or_val'))

IN = namedtuple('IN', ('reg', 'reg_or_val'))

JUMP = namedtuple('JUMP', ('label_or_ind', 'label'))

LOAD = namedtuple('LOAD', ('reg', 'reg_or_val'))

OR = namedtuple('OR', ('reg', 'reg_or_val'))

OUT = namedtuple('OUT', ('reg', 'reg_or_val'))

RET = namedtuple('RET', ('indicator',))

RETI = namedtuple('RETI', ('flag',))

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

STORE = namedtuple('STORE', ('reg', 'reg_or_val'))

SUB = namedtuple('SUB', ('reg', 'reg_or_val'))

SUBC = namedtuple('SUBC', ('reg', 'reg_or_val'))

TEST = namedtuple('TEST', ('reg', 'reg_or_val'))

XOR = namedtuple('XOR', ('reg', 'reg_or_val'))

""" DIRECTIVES """

ORG = namedtuple('ORG', ('addr',))

EQU = namedtuple('EQU', ('alias', 'reg_or_val'))

DSIN = namedtuple('DSIN', ('alias', 'pp'))
DSOUT = namedtuple('DSOUT', ('alias', 'pp'))
DSIO = namedtuple('DSIO', ('alias', 'pp'))

LABEL = namedtuple('LABEL', ('alias',))

MNEMONICS = {
    i.__name__: i for i in (ADD, ADDC, AND, CALL, COMP, DINT, EINT, FETCH, IN, JUMP, LOAD, OR, OUT, RET,
                            RETI, RL, SL0, SL1, SLA, SLX, RR, SR0, SR1, SRA, SRX, STORE, SUB, SUBC, TEST, XOR,
                            ORG, EQU, DSIN, DSOUT, DSIO)
}
