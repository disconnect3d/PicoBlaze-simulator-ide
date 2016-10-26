# this file is used by ply.yacc
from instructions import AVAILABLE_INSTRUCTIONS, Equ


class ParseException(Exception):
    pass


class Parser(object):
    def __init__(self):
        self._instructions = []

    @property
    def instructions(self):
        return self._instructions

    def _add(self, instruction):
        if type(instruction) not in AVAILABLE_INSTRUCTIONS:
            raise ParseException('Unrecognized instruction type: %s' % type(instruction))

        self._instructions.append(instruction)

    def p_instruction(self, p):
        """instruction : normal_instruction
                       | equ_instruction"""
        print('instruction', p)
        return p

    def p_normal_instruction(self, p):
        """normal_instruction : INSTRUCTION REGISTER COMMA REGISTER"""
        print("normal instruction", p)
        return p

    def p_equ_instruction(self, p):
        """equ_instruction : NAME INSTRUCTION NUMBER
                           | NAME INSTRUCTION REGISTER"""
        _, name, equ, value = p

        if equ.upper() != 'EQU':
            raise ParseException('Incorrect instruction, EQU expected.')

        self._add(Equ(alias=name, value=value))

        return p

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input: ", p)
