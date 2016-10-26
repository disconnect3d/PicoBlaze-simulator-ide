import pytest
from ply import lex

import tokenizer_rules
from errors import TokenizeException


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
    assert get_tokens('; this should not be added to tokens...') == []


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
        EQU equ Equ eQu EqU EQu eQU
        ADD add Add ADd aDD adD
    '''

    expected = [('INSTRUCTION', 'LOAD')] * 5
    expected += [('INSTRUCTION', 'EQU')] * 7
    expected += [('INSTRUCTION', 'ADD')] * 6

    assert get_tokens(code) == expected


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
