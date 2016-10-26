from collections import namedtuple


Load = namedtuple('Load', ('register', 'reg_or_val'))

Equ = namedtuple('Equ', ('alias', 'value'))
Org = namedtuple('Org', ('address',))

AVAILABLE_INSTRUCTIONS = {
    i: i.__name__.upper() for i in (Equ, Load)
}
