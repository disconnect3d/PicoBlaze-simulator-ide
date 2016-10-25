# this file is used by ply.yacc

import ply.yacc as yacc
from ply import lex

import tokenizer_rules
from tokenizer_rules import tokens


class Parser(object):
    def __init__(self):
        self.instructions = []

    def p_normal_instruction(self, p):
        """normal_instruction : INSTRUCTION REGISTER COMMA REGISTER"""
        print("normal instruction", p)
        return p


    def p_equ_instruction(self, p):
        """equ_instruction : NAME INSTRUCTION NUMBER"""
        print("EQu inst", p)
        return p


    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")
