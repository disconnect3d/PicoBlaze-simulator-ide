# this file is used by ply.yacc
from src.errors import ParseException
from src.mnemonics import MNEMONICS, EQU, ORG, LABEL
import re


class Parser(object):
    def __init__(self):
        self._instructions = []
        self._directives = []
        self._aliases = {}

    def reset_state(self):
        self._instructions = []
        self._directives = []
        self._aliases = {}

    @property
    def instructions(self):
        return self._instructions

    @property
    def aliases(self):
        return self._aliases

    @property
    def directives(self):
        return self._directives

    def _add_code(self, instruction):
        self._instructions.append(instruction)

    def _add_directive(self, directive):
        self._directives.append(directive)

    def _add_alias(self, key, val):
        self._aliases[key] = val

    def p_line(self, p):
        """line : instruction inline_comment
                | directive   inline_comment
                | label       inline_comment
                | label_instr inline_comment
                | comment"""
        return p

    def p_instruction(self, p):
        """instruction : reg_val_instruction
                       | reg_instruction
                       | no_arg_instruction
                       | jump_ind_instruction
                       | ret_ind_instruction
                       | reti_flag_instruction"""
        return p

    def p_reg_val_instruction(self, p):
        """reg_val_instruction : ADD   reg_or_alias COMMA reg_num_alias
                               | ADDC  reg_or_alias COMMA reg_num_alias
                               | AND   reg_or_alias COMMA reg_num_alias
                               | COMP  reg_or_alias COMMA reg_num_alias
                               | FETCH reg_or_alias COMMA reg_num_alias
                               | IN    reg_or_alias COMMA reg_num_alias
                               | LOAD  reg_or_alias COMMA reg_num_alias
                               | OR    reg_or_alias COMMA reg_num_alias
                               | OUT   reg_or_alias COMMA reg_num_alias
                               | STORE reg_or_alias COMMA reg_num_alias
                               | SUB   reg_or_alias COMMA reg_num_alias
                               | SUBC  reg_or_alias COMMA reg_num_alias
                               | TEST  reg_or_alias COMMA reg_num_alias
                               | XOR   reg_or_alias COMMA reg_num_alias"""
        _, instruction, arg1, _, arg2 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1, arg2)

        self._add_code(instruction_obj)

        return p

    def p_reg_instruction(self, p):
        """reg_instruction : RL reg_or_alias
                           | RR reg_or_alias
                           | SL0 reg_or_alias
                           | SL1 reg_or_alias
                           | SLA reg_or_alias
                           | SLX reg_or_alias
                           | SR0 reg_or_alias
                           | SR1 reg_or_alias
                           | SRA reg_or_alias
                           | SRX reg_or_alias
                            """
        _, instruction, arg1 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1)

        self._add_code(instruction_obj)

        return p

    def p_jump_ind_instruction(self, p):
        """jump_ind_instruction : CALL NAME
                                | CALL INDICATOR COMMA NAME
                                | CALL NUMBER
                                | CALL INDICATOR COMMA NUMBER
                                | JUMP NAME
                                | JUMP INDICATOR COMMA NAME
                                | JUMP NUMBER
                                | JUMP INDICATOR COMMA NUMBER"""

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
        _, instruction = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction]()

        self._add_code(instruction_obj)

        return p

    def p_ret_ind_instruction(self, p):
        """ret_ind_instruction : RET
                               | RET INDICATOR"""
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
        _, instruction, arg1 = p

        if instruction not in MNEMONICS:
            raise ParseException('Unrecognized instruction: %s' % instruction)

        instruction_obj = MNEMONICS[instruction](arg1)

        self._add_code(instruction_obj)

        return p

    def p_reg_or_alias(self, p):
        """reg_or_alias : REGISTER
                        | NAME"""
        regs = re.compile('(?i)s((1[0-5]|[0-9])|(?i)[a-f])')
        _, arg = p
        if not regs.match(arg):
            if arg not in self._aliases.keys():
                raise ParseException('Name "{0}" not defined'.format(arg))
            else:
                arg = self._aliases[arg]

        p[0] = arg

    def p_reg_num_alias(self, p):
        """reg_num_alias : REGISTER
                         | NUMBER
                         | NAME"""
        regs = re.compile('(?i)s((1[0-5]|[0-9])|(?i)[a-f])')
        _, arg = p
        if not type(arg) is int and not regs.match(arg):
            if arg not in self.aliases.keys():
                raise ParseException('Name "{0}" not defined'.format(arg))
            else:
                arg = self._aliases[arg]

        p[0] = arg

    def p_inline_comment(self, p):
        """inline_comment :
                          | COMMENT"""
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

        self._add_directive(EQU(alias=name, reg_or_val=arg))
        self._add_alias(name, arg)

        return p

    def p_ds_directive(self, p):
        """ds_directive : NAME DSIN NUMBER
                        | NAME DSOUT NUMBER
                        | NAME DSIO NUMBER"""

        _, name, directive, arg = p

        if directive not in MNEMONICS:
            raise ParseException('Unrecognized directive: %s' % directive)

        directive_obj = MNEMONICS[directive](name, arg)

        self._add_directive(directive_obj)
        # TODO there could be some fancy check or split into 3 dicts
        # TODO althoug for pBlaze simulator they are normal aliases
        self._add_alias(name, arg)

        return p

    def p_label(self, p):
        """label : LABEL"""
        _, label, *_ = p

        self._add_code(LABEL(alias=label))

        return p

    def p_label_instr(self, p):
        """label_instr : LABEL instruction"""
        _, label, *_ = p

        self.instructions.insert(len(self.instructions)-1, LABEL(alias=label))

        return p

    def p_comment(self, p):
        """comment : COMMENT"""
        return p

    # Error rule for syntax errors
    def p_error(self, p):
        raise ParseException('Parse error in input {0}:{1}: wrong symbol "{2}"'.format(p.lineno, p.lexpos, p.value))
