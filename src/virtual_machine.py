from src.parser_rules import Parser
from src.mnemonics import *
from src.uint8 import uint8
from ply import lex, yacc
from collections import OrderedDict
import src.tokenizer_rules as tokenizer_rules


class VirtualMachine(object):
    def __init__(self):
        self._parser = Parser()
        self._registers = OrderedDict([('S'+str(i), uint8(0)) for i in [*range(10), *[j for j in 'ABCDEF']]])
        self._instructions = {addr: None for addr in range(1024)}
        self._ram = {addr: uint8(0) for addr in range(64)}
        self._labels = {}
        self._carry = 0
        self._zero = 0
        self._stack = []

        self._interrupt_enabled = False
        self._pre_zero = 0
        self._pre_carry = 0
        self._interrupt_caused = False

        self._program_cnt = 0

        lex.lex(module=tokenizer_rules)
        self._parser.tokens = tokenizer_rules.tokens
        self._yacc = yacc.yacc(module=self._parser)

        self.__handlers = {
            ADD:   self._handle_ADD,
            ADDC:  self._handle_ADDC,
            AND:   self._handle_AND,
            CALL:  self._handle_CALL,
            COMP:  self._handle_COMP,
            DINT:  self._handle_DINT,
            EINT:  self._handle_EINT,
            FETCH: self._handle_FETCH,
            IN:    self._handle_IN,
            JUMP:  self._handle_JUMP,
            LOAD:  self._handle_LOAD,
            OR:    self._handle_OR,
            OUT:   self._handle_OUT,
            RET:   self._handle_RET,
            RETI:  self._handle_RETI,
            RL:    self._handle_RL,
            SL0:   self._handle_SL0,
            SL1:   self._handle_SL1,
            SLA:   self._handle_SLA,
            SLX:   self._handle_SLX,
            RR:    self._handle_RR,
            SR0:   self._handle_SR0,
            SR1:   self._handle_SR1,
            SRA:   self._handle_SRA,
            SRX:   self._handle_SRX,
            STORE: self._handle_STORE,
            SUB:   self._handle_SUB,
            SUBC:  self._handle_SUBC,
            TEST:  self._handle_TEST,
            XOR:   self._handle_XOR,
        }

    @property
    def registers(self):
        return self._registers

    @property
    def ram(self):
        return self._ram

    def parse_file(self, filename):
        with open(filename) as file:
            content = file.readlines()

        for i in content:
            self._yacc.parse(i)

        instruction_cnt = 0
        for i in self._parser.instructions:
            if type(i) == ORG:
                if instruction_cnt <= i[0]:
                    instruction_cnt = i[0]
                else:
                    raise ValueError(str(i) + ": Trying to place code in past position")
            elif type(i) == LABEL:
                if i[0] not in self._labels:
                    self._labels[i[0]] = instruction_cnt
                else:
                    raise ValueError(str(i) + ": Label already in use")
            else:
                self._instructions[instruction_cnt] = i
                instruction_cnt += 1

    def _handle_LOAD(self, *args):
        self.registers[args[0]] = uint8(args[1])
        self._program_cnt += 1

    def _handle_FETCH(self, *args):
        if args[1] < 0 or args[1] > 63:
            raise ValueError('Error in address {0}: ram addres "{1}" outside memory'.format(
                             str(self._program_cnt), args[1]))
        self.registers[args[0]] = self.ram[args[1]]
        self._program_cnt += 1

    def _handle_STORE(self, *args):
        if args[1] < 0 or args[1] > 63:
            raise ValueError('Error in address {0}: ram addres "{1}" outside memory'.format(
                str(self._program_cnt), args[1]))
        self.ram[args[1]] = self.registers[args[0]]
        self._program_cnt += 1

    def _handle_IN(self, *args):
        # there could be some port simulator in further version of VM class,
        # for now we assume that there are only zeros on input
        if args[1] < 0 or args[1] > 63:
            raise ValueError('Error in address {0}: no such port "{1}"'.format(
                str(self._program_cnt), args[1]))
        self.registers[args[0]] = uint8(0)
        self._program_cnt += 1

    def _handle_OUT(self, *args):
        # output to /dev/null
        if args[1] < 0 or args[1] > 63:
            raise ValueError('Error in address {0}: no such port "{1}"'.format(
                str(self._program_cnt), args[1]))
        self._program_cnt += 1

    def _handle_ADD(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] + args[1]
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_ADDC(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] + (args[1] + self._carry)
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_SUB(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] - args[1]
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_SUBC(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] - (args[1] - self._carry)
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_COMP(self, *args):
        self._zero = 1 if self.registers[args[0]] is args[1] else 0
        self._carry = 1 if self.registers[args[0]] < args[1] else 0
        self._program_cnt += 1

    def _handle_AND(self, *args):
        self.registers[args[0]] &= args[1]
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_OR(self, *args):
        self.registers[args[0]] |= args[1]
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_XOR(self, *args):
        self.registers[args[0]] ^= args[1]
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_TEST(self, *args):
        def bit_parity(num):
            bits = num.as_bit_list()
            result = bits[0]
            for i in bits[1:]:
                result ^= i
            return result

        self._zero = 1 if (self.registers[args[0]] & args[1]) is 0 else 0
        self._carry = 1 if bit_parity(self.registers[args[0]] & args[1]) is 1 else 0
        self._program_cnt += 1

    def _handle_SL0(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] << 1
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_SL1(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] << 1
        self.registers[args[0]] |= 1
        self._program_cnt += 1

    def _handle_SLX(self, *args):
        rest = self.registers[args[0]][0]
        self.registers[args[0]], self._carry = self.registers[args[0]] << 1
        self.registers[args[0]] |= rest
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_SLA(self, *args):
        carry = self._carry
        self.registers[args[0]], self._carry = self.registers[args[0]] << 1
        self.registers[args[0]] |= carry
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_RL(self, *args):
        rest = self.registers[args[0]][7]
        self.registers[args[0]], self._carry = self.registers[args[0]] << 1
        self.registers[args[0]] |= rest
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_SR0(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] >> 1
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_SR1(self, *args):
        self.registers[args[0]], self._carry = self.registers[args[0]] >> 1
        self.registers[args[0]] |= 1 << 7
        self._program_cnt += 1

    def _handle_SRX(self, *args):
        rest = self.registers[args[0]][7]
        self.registers[args[0]], self._carry = self.registers[args[0]] >> 1
        self.registers[args[0]] |= rest << 7
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_SRA(self, *args):
        carry = self._carry
        self.registers[args[0]], self._carry = self.registers[args[0]] >> 1
        self.registers[args[0]] |= carry << 7
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_RR(self, *args):
        rest = self.registers[args[0]][0]
        self.registers[args[0]], self._carry = self.registers[args[0]] >> 1
        self.registers[args[0]] |= rest << 7
        self._zero = 1 if self.registers[args[0]] == 0 else 0
        self._program_cnt += 1

    def _handle_JUMP(self, *args):
        if args[1] is not None:
            if type(args[1]) is str:
                if args[1] not in self._labels.keys():
                    raise KeyError('Error in address {0}: no such label "{1}"'.format(str(self._program_cnt), args[1]))
                else:
                    arg2 = self._labels[args[1]]
            else:
                if args[1] < 0 or args[1] > 1023:
                    raise ValueError('Error in address {0}: no such address "{1}"'.format(str(self._program_cnt), args[1]))
                else:
                    arg2 = args[1]
            if args[0] == 'Z' and self._zero == 1 or \
               args[0] == 'NZ' and self._zero == 0 or \
               args[0] == 'C' and self._carry == 1 or \
               args[0] == 'NC' and self._carry == 0:
                self._program_cnt = arg2
            else:
                self._program_cnt += 1
        else:
            if type(args[0]) is str:
                if args[0] not in self._labels.keys():
                    raise KeyError('Error in address {0}: no such label "{1}"'.format(str(self._program_cnt), args[0]))
                else:
                    arg1 = self._labels[args[0]]
            else:
                if args[0] < 0 or args[0] > 1023:
                    raise ValueError('Error in address {0}: no such address "{1}"'.format(str(self._program_cnt), args[0]))
                else:
                    arg1 = args[0]
            self._program_cnt = arg1

    def _handle_CALL(self, *args):
        if args[1] is not None:
            if type(args[1]) is str:
                if args[1] not in self._labels.keys():
                    raise KeyError('Error in address {0}: no such label "{1}"'.format(str(self._program_cnt), args[1]))
                else:
                    arg2 = self._labels[args[1]]
            else:
                if args[1] < 0 or args[1] > 1023:
                    raise ValueError('Error in address {0}: no such address "{1}"'.format(str(self._program_cnt), args[1]))
                else:
                    arg2 = args[1]
            if args[0] == 'Z' and self._zero == 1 or \
               args[0] == 'NZ' and self._zero == 0 or \
               args[0] == 'C' and self._carry == 1 or \
               args[0] == 'NC' and self._carry == 0:
                self._stack.append(self._program_cnt)
                self._program_cnt = arg2
            else:
                self._program_cnt += 1
        else:
            if type(args[0]) is str:
                if args[0] not in self._labels.keys():
                    raise KeyError('Error in address {0}: no such label "{1}"'.format(str(self._program_cnt), args[0]))
                else:
                    arg1 = self._labels[args[0]]
            else:
                if args[0] < 0 or args[0] > 1023:
                    raise ValueError('Error in address {0}: no such address "{1}"'.format(str(self._program_cnt), args[0]))
                else:
                    arg1 = args[0]
            self._stack.append(self._program_cnt)
            self._program_cnt = arg1

    def _handle_RET(self, *args):
        if args[0] is not None:
            if args[0] == 'Z' and self._zero == 1 or \
               args[0] == 'NZ' and self._zero == 0 or \
               args[0] == 'C' and self._carry == 1 or \
               args[0] == 'NC' and self._carry == 0:
                self._program_cnt = self._stack.pop() + 1
            else:
                self._program_cnt += 1
        else:
            self._program_cnt = self._stack.pop() + 1

    def _handle_DINT(self, *args):
        self._interrupt_enabled = 0
        self._program_cnt += 1

    def _handle_EINT(self, *args):
        self._interrupt_enabled = 1
        self._program_cnt += 1

    def _handle_RETI(self, *args):
        if args[0] == 'ENABLE':
            self._interrupt_enabled = True
        else:
            self._interrupt_enabled = False
        self._carry = self._pre_carry
        self._zero = self._pre_zero
        self._program_cnt = self._stack.pop()

    def _handle_interrupt(self):
        self._pre_carry = self._carry
        self._pre_zero = self._zero
        self._interrupt_enabled = False
        self._stack.append(self._program_cnt)
        self._program_cnt = 1023

    def step_over(self):
        if self._interrupt_caused and self._interrupt_enabled:
            self._handle_interrupt()
            return

        if self._program_cnt > 1023:
            raise RuntimeError("Out of memory range")

        instruction = self._instructions[self._program_cnt]
        if instruction is not None:
            if len(instruction) is 2 and instruction[1] in self._registers:
                arg2 = self._registers[instruction[1]]
                self.__handlers[type(instruction)](instruction[0], arg2)
            else:
                self.__handlers[type(instruction)](*instruction)
        else:
            self._program_cnt += 1

    def toggle_interrupt(self, state):
        self._interrupt_caused = state

    def print_parameters(self):
        for k, val in self._registers.items():
            print('{0}: {1} ({2})'.format(k, str(val).rjust(3), bin(val)[2:].zfill(8)))
        print("Zero: {0}  Carry: {1}  Interrupt enabled: {2}".format(self._zero, self._carry, self._interrupt_enabled))
        print("Program counter: {0}".format(self._program_cnt))

    def step_many(self, amount, print_params=False):
        for i in range(amount):
            self.step_over()
            if print_params:
                self.print_parameters()


