from collections import namedtuple


Equ = namedtuple('Equ', ('alias', 'value'))
Load = namedtuple('Load', ('register', 'address'))

AVAILABLE_INSTRUCTIONS = (Equ, Load)
