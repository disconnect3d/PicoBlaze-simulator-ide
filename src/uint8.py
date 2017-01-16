class uint8(object):
    _mask = 0b11111111

    def __init__(self, value):
        self._val = value & self._mask

    def __add__(self, other):
        if isinstance(other, int):
            result = self._val + other
        else:
            result = self._val + other._val

        if result > self._mask or result < 0:
            return uint8(result), 1
        else:
            return uint8(result), 0

    def __sub__(self, other):
        if isinstance(other, int):
            result = self._val - other
        else:
            result = self._val - other._val

        if result > self._mask or result < 0:
            return uint8(result), 1
        else:
            return uint8(result), 0

    def __and__(self, other):
        if isinstance(other, int):
            return uint8(self._val & other)
        else:
            return uint8(self._val & other._val)

    def __or__(self, other):
        if isinstance(other, int):
            return uint8(self._val | other)
        else:
            return uint8(self._val | other._val)

    def __xor__(self, other):
        if isinstance(other, int):
            return uint8(self._val ^ other)
        else:
            return uint8(self._val ^ other._val)

    def __mod__(self, other):
        if isinstance(other, int):
            return uint8(self._val % other)
        else:
            return uint8(self._val % other._val)

    def __lshift__(self, other):
        return uint8(self._val << other), self[7]

    def __rshift__(self, other):
        return uint8(self._val >> other), self[0]

    def __getitem__(self, item):
        if item < 0 or item > 7:
            raise ValueError("Wrong agrument")
        return (self._val >> item) & 1

    def __eq__(self, other):
        if isinstance(other, int):
            return self._val == other
        else:
            return self._val == other._val

    def __lt__(self, other):
        if isinstance(other, int):
            return self._val < other
        else:
            return self._val < other._val

    def __bool__(self):
        return False if self._val is 0 else True

    def __int__(self):
        return self._val

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return str(self._val)

    def __index__(self):
        return self._val

    def as_bit_list(self):
        return [int(i) for i in bin(self._val)[2:]]

    def as_bit_str(self):
        return bin(self._val)[2:]
