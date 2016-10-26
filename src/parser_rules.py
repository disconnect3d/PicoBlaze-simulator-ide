# this file is used by ply.yacc


class Parser(object):
    def __init__(self):
        self.instructions = []

    def p_normal_instruction(self, p):
        """normal_instruction : INSTRUCTION REGISTER COMMA REGISTER"""
        print("normal instruction", p)
        return p


    def p_equ_instruction(self, p):
        """equ_instruction : NAME INSTRUCTION NUMBER"""
        print("EQu inst", p, p[0], p[1], p[2], p[3])
        return p


    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")
