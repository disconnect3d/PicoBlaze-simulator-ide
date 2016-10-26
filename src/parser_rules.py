# this file is used by ply.yacc
from errors import ParseException
from mnemonics import AVAILABLE_INSTRUCTIONS, Equ, Org


class Parser(object):
    def __init__(self):
        self._instructions = []

    def reset_state(self):
        self._instructions = []

    @property
    def instructions(self):
        return self._instructions

    def _add_code(self, instruction):
        self._instructions.append(instruction)


    def p_line(self, p):
        """line : instruction
                | directive"""
        print('instruction', p)
        return p

    def p_instruction(self, p):
        """instruction : INSTRUCTION REGISTER COMMA REGISTER
                       | INSTRUCTION REGISTER COMMA NUMBER
                       | INSTRUCTION NUMBER COMMA REGISTER
                       | INSTRUCTION NUMBER COMMA NUMBER"""
        print("normal instruction", p)
        _, instruction, arg1, _, arg2 = p

        if instruction not in AVAILABLE_INSTRUCTIONS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = AVAILABLE_INSTRUCTIONS[instruction](arg1, arg2)

        self._add_code(instruction_obj)

        return p

    def p_directive(self, p):
        """directive : equ_directive
                     | org_directive"""
        return p

    def p_org_directive(self, p):
        """org_directive : DIRECTIVE NUMBER"""
        _, directive, address = p

        if directive != 'ORG':
            raise ParseException('Incorrect directive, ORG expected')

        self._add_code(Org(address=address))

        return p

    def p_equ_directive(self, p):
        """equ_directive : NAME DIRECTIVE NUMBER
                         | NAME DIRECTIVE REGISTER"""
        _, name, directive, value = p

        if directive != 'EQU':
            raise ParseException('Incorrect instruction, EQU expected.')

        self._add_code(Equ(alias=name, value=value))

        return p

    # Error rule for syntax errors
    def p_error(self, p):
        raise ParseException("Syntax error in input: '%s'" % p)
