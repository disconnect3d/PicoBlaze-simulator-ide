import pytest
from ply import lex

import src.tokenizer_rules as tokenizer_rules
from src.errors import TokenizeException


@pytest.fixture(scope='session')
def lexer():
    return lex.lex(module=tokenizer_rules)


@pytest.fixture(scope='session')
def get_tokens(lexer):
    def _tokens_gen(input_string):
        lexer.input(input_string)

        return [(token.type, token.value) for token in lexer]

    return _tokens_gen


def test_comment(get_tokens):
    assert get_tokens('; comment...') == [('COMMENT', '; comment...')]


def test_numbers(get_tokens):
    assert get_tokens('123 $0e $FF $3fF') == [
        ('NUMBER', 123),
        ('NUMBER', 14),
        ('NUMBER', 255),
        ('NUMBER', 1023)
    ]


def test_instructions(get_tokens):
    code = '''
        LOAD load lOaD LoAD loaD
        ADD add Add ADd aDD adD
        ADDC addc Addc ADdC aDDc adDC
    '''
    instructions = 'STORE FETCH JUMP CALL RET RETI ADD ADDC SUB SUBC XOR OR AND IN OUT EINT DINT COMP'

    expected = [('LOAD', 'LOAD')] * 5
    expected += [('ADD', 'ADD')] * 6
    expected += [('ADDC', 'ADDC')] * 6
    assert get_tokens(code) == expected
    assert get_tokens(instructions) == [(instr, instr) for instr in instructions.split(' ')]


def test_directives(get_tokens):
    assert get_tokens('EQU equ EqU') == [('EQU', 'EQU')] * 3
    assert get_tokens('ORG org oRg') == [('ORG', 'ORG')] * 3
    assert get_tokens('DSIN dsin dSiN') == [('DSIN', 'DSIN')] * 3
    assert get_tokens('DSOUT dsout dSoUt') == [('DSOUT', 'DSOUT')] * 3
    assert get_tokens('DSIO dsio DsIo') == [('DSIO', 'DSIO')] * 3


def test_registers(get_tokens):
    regs_dec = [('REGISTER', 'S%d' % i) for i in range(0, 16)]
    regs_hex = [('REGISTER', 'S%s' % s) for s in 'AABBCCDDEEFF']

    assert get_tokens('s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 s14 s15') == regs_dec
    assert get_tokens('sa sA sb sB sc sC sd sD se sE sf sF') == regs_hex
    assert get_tokens('S0 S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11 S12 S13 S14 S15') == regs_dec
    assert get_tokens('Sa SA Sb SB Sc SC Sd SD Se SE Sf SF') == regs_hex


def test_label_and_comma(get_tokens):
    assert get_tokens('label1: LABEL2: lab_el3: lab__442: ') == [
        ('LABEL', l) for l in ('label1', 'LABEL2', 'lab_el3', 'lab__442')
        ]

    assert get_tokens(',    , ,') == [('COMMA', ',')] * 3


def test_unrecognized_token(get_tokens):
    for prefix in ':@#$%^&*()':
        with pytest.raises(TokenizeException):
            get_tokens(' %s ' % prefix)

    for suffix in '@#$%^&*()':
        with pytest.raises(TokenizeException):
            get_tokens(' name%s ' % suffix)


def test_name(get_tokens):
    assert get_tokens('Something else but these should be names') == [
        ('NAME', n) for n in ('Something', 'else', 'but', 'these', 'should', 'be', 'names')
        ]


def test_indicators(get_tokens):
    assert get_tokens('z nz c nc Z NZ C NC nZ nC Nz Nc') == [
        ('INDICATOR', i) for i in ('Z', 'NZ', 'C', 'NC', 'Z', 'NZ', 'C', 'NC', 'NZ', 'NC', 'NZ', 'NC')
    ]


def test_flags(get_tokens):
    assert get_tokens('ENABLE enable eNaBlE') == [('FLAG', 'ENABLE')]*3
    assert get_tokens('DISABLE disable DiSaBlE') == [('FLAG', 'DISABLE')]*3

