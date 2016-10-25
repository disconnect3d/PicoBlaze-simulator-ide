

class Register(object):
    def __init__(self, bits):
        self._v = 0
        self.min_value = 0
        self.max_value = 2**bits - 1


GENERAL_PURPOSE_REGS = 16

GP_REGISTER_BITS = 8
RAM_BYTES = 64
PC_BITS = 10


class VMMemory(object):
    def __init__(self, mem_bytes):
        self._mem = bytearray(mem_bytes)

    def _is_valid_addr(self, addr):
        if addr < 0 or addr >= len(self._mem):
                return False

        return True

    def fetch_byte(self, addr):
        if self._is_valid_addr(addr):
            return None

        return self._mem[addr]

    def store_byte(self, addr, value):
        if self._is_valid_addr(addr):
            return False

        self._mem[addr] = value
        return True


class VMInstance(object):
    def __init__(self):
        self.r = [Register(GP_REGISTER_BITS) for _ in range(GENERAL_PURPOSE_REGS)]
        self.pc = Register(PC_BITS)
        #self.stack
        self._ram = VMMemory(RAM_BYTES)

