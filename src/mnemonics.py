from collections import namedtuple


LOAD = namedtuple('LOAD', ('reg', 'reg_or_val'))

EQU = namedtuple('EQU', ('alias', 'arg'))
ORG = namedtuple('ORG', ('addr',))

SUB = namedtuple('SUB', ('reg', 'arg'))
ADD = namedtuple('ADD', ('reg', 'arg'))

ADDC = namedtuple('ADDC', ('reg', 'arg'))
SUBC = namedtuple('SUBC', ('reg', 'arg'))

XOR = namedtuple('XOR', ('reg', 'arg'))
OR = namedtuple('OR', ('reg', 'arg'))
AND = namedtuple('AND', ('reg', 'arg'))

LABEL = namedtuple('LABEL', ('alias',))

MNEMONICS = {
    i.__name__: i for i in (LOAD, EQU, ORG, SUB, ADD, ADDC, SUBC, XOR, OR, AND, LABEL)
}
