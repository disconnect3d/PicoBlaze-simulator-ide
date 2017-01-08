# this file is used by ply.yacc
from src.errors import ParseException
from src.mnemonics import MNEMONICS, EQU, ORG, LABEL

# TODO validation


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
                | label
                | comment"""
        print('line', p)
        return p

    def p_instruction(self, p):
        """instruction : reg_val_instruction
                       | reg_instruction
                       | no_arg_instruction
                       | jump_ind_instruction
                       | ret_ind_instruction
                       | reti_flag_instruction"""
        print("normal instruction", p)

        return p

    def p_reg_val_instruction(self, p):
        """reg_val_instruction : ADD REGISTER COMMA REGISTER
                               | ADD REGISTER COMMA NUMBER
                               | ADDC REGISTER COMMA REGISTER
                               | ADDC REGISTER COMMA NUMBER
                               | AND REGISTER COMMA REGISTER
                               | AND REGISTER COMMA NUMBER
                               | COMP REGISTER COMMA REGISTER
                               | COMP REGISTER COMMA NUMBER
                               | FETCH REGISTER COMMA REGISTER
                               | FETCH REGISTER COMMA NUMBER
                               | IN REGISTER COMMA REGISTER
                               | IN REGISTER COMMA NUMBER
                               | LOAD REGISTER COMMA REGISTER
                               | LOAD REGISTER COMMA NUMBER
                               | OR REGISTER COMMA REGISTER
                               | OR REGISTER COMMA NUMBER
                               | OUT REGISTER COMMA REGISTER
                               | OUT REGISTER COMMA NUMBER
                               | STORE REGISTER COMMA REGISTER
                               | STORE REGISTER COMMA NUMBER
                               | SUB REGISTER COMMA REGISTER
                               | SUB REGISTER COMMA NUMBER
                               | SUBC REGISTER COMMA REGISTER
                               | SUBC REGISTER COMMA NUMBER
                               | TEST REGISTER COMMA REGISTER
                               | TEST REGISTER COMMA NUMBER
                               | XOR REGISTER COMMA REGISTER
                               | XOR REGISTER COMMA NUMBER"""
        print("reg_or_val instruction", p)
        _, instruction, arg1, _, arg2 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1, arg2)

        self._add_code(instruction_obj)

        return p

    def p_reg_instruction(self, p):
        """reg_instruction : RL REGISTER
                           | RR REGISTER
                           | SL0 REGISTER
                           | SL1 REGISTER
                           | SLA REGISTER
                           | SLX REGISTER
                           | SR0 REGISTER
                           | SR1 REGISTER
                           | SRA REGISTER
                           | SRX REGISTER
                            """
        print("reg instruction", p)
        _, instruction, arg1 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1)

        self._add_code(instruction_obj)

        return p

    def p_jump_ind_instruction(self, p):
        """jump_ind_instruction : CALL NAME
                                | CALL INDICATOR COMMA NAME
                                | JUMP NAME
                                | JUMP INDICATOR COMMA NAME"""

        print("jump indicator instruction", p)
        arg2 = None
        if len(p) > 3:
            _, instruction, arg1, _, arg2 = p
        else:
            _, instruction, arg1 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1, arg2)

        self._add_code(instruction_obj)

        return p

    def p_no_arg_instruction(self, p):
        """no_arg_instruction : DINT
                              | EINT"""
        print("no arg instruction", p)
        _, instruction = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction]()

        self._add_code(instruction_obj)

        return p

    def p_ret_ind_instruction(self, p):
        """ret_ind_instruction : RET
                               | RET INDICATOR"""
        print("ret indicator instruction", p)
        arg1 = None
        if len(p) > 2:
            _, instruction, arg1 = p
        else:
            _, instruction = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1)

        self._add_code(instruction_obj)

        return p

    def p_reti_flag_instruction(self, p):
        """reti_flag_instruction : RETI FLAG"""
        print("reti flag instruction", p)
        _, instruction, arg1 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1)

        self._add_code(instruction_obj)

        return p

    def p_directive(self, p):
        """directive : equ_directive
                     | org_directive
                     | ds_directive"""
        return p

    def p_org_directive(self, p):
        """org_directive : ORG NUMBER"""
        _, directive, addr = p

        if directive != 'ORG':
            raise ParseException('Incorrect directive, ORG expected')

        self._add_code(ORG(addr=addr))

        return p

    def p_equ_directive(self, p):
        """equ_directive : NAME EQU NUMBER
                         | NAME EQU REGISTER"""
        _, name, directive, arg = p

        if directive != 'EQU':
            raise ParseException('Incorrect instruction, EQU expected.')

        self._add_code(EQU(alias=name, reg_or_val=arg))

        return p

    def p_ds_directive(self, p):
        """ds_directive : NAME DSIN NUMBER
                        | NAME DSOUT NUMBER
                        | NAME DSIO NUMBER"""

        _, name, directive, arg = p

        if directive not in MNEMONICS:
            raise ParseException('Unrecognized directive: %s' % directive)

        directive_obj = MNEMONICS[directive](name, arg)

        self._add_code(directive_obj)

        return p

    def p_label(self, p):
        """label : LABEL
                 | LABEL instruction"""
        _, label, *_ = p

        self._add_code(LABEL(alias=label))

        return p

    def p_comment(self, p):
        """comment : COMMENT"""
        return p

    # Error rule for syntax errors
    def p_error(self, p):
        raise ParseException("Syntax error in input: '%s'" % p)
