# this file is used by ply.yacc
from src.errors import ParseException
from src.mnemonics import MNEMONICS, EQU, ORG, LABEL


class Parser(object):
    def __init__(self):
        self._instructions = []

    def reset_state(self):
        self._instructions = []

    @property
    def instructions(self):
        return self._instructions

    def _add_code(self, instruction):
        self._instructions.insert(0, instruction)

    def p_line(self, p):
        """line : instruction
                | directive
                | label"""
        print('instruction', p)
        return p

    def p_instruction(self, p):
        """instruction : INSTRUCTION REGISTER COMMA REGISTER
                       | INSTRUCTION REGISTER COMMA NUMBER
                       | INSTRUCTION NUMBER COMMA REGISTER
                       | INSTRUCTION NUMBER COMMA NUMBER"""
        print("normal instruction", p)
        _, instruction, arg1, _, arg2 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1, arg2)

        self._add_code(instruction_obj)

        return p

    def p_directive(self, p):
        """directive : equ_directive
                     | org_directive"""
        return p

    def p_org_directive(self, p):
        """org_directive : DIRECTIVE NUMBER"""
        _, directive, addr = p

        if directive != 'ORG':
            raise ParseException('Incorrect directive, ORG expected')

        self._add_code(ORG(addr=addr))

        return p

    def p_equ_directive(self, p):
        """equ_directive : NAME DIRECTIVE NUMBER
                         | NAME DIRECTIVE REGISTER"""
        _, name, directive, arg = p

        if directive != 'EQU':
            raise ParseException('Incorrect instruction, EQU expected.')

        self._add_code(EQU1(alias=name, arg=arg))

        return p

    def p_label(self, p):
        """label : LABEL
                 | LABEL instruction"""
        _, label, *_ = p

        self._add_code(LABEL(alias=label))

        return p

    # Error rule for syntax errors
    def p_error(self, p):
        raise ParseException("Syntax error in input: '%s'" % p)
