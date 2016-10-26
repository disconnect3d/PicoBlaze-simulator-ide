import pytest
from ply import lex

import tokenizer_rules


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


def test_load(get_tokens):
    assert get_tokens('LOAD s0, 123') == [
        ('INSTRUCTION', 'LOAD'),
        ('REGISTER', 's0'),
        ('COMMA', ','),
        ('NUMBER', 123)
    ]


def test_add_value(get_tokens):
    assert get_tokens('ADD s5, 23') == [
        ('INSTRUCTION', 'ADD'),
        ('REGISTER', 's5'),
        ('COMMA', ','),
        ('NUMBER', 23)
    ]


def test_add_regs(get_tokens):
    assert get_tokens('ADD s1, s2') == [
        ('INSTRUCTION', 'ADD'),
        ('REGISTER', 's1'),
        ('COMMA', ','),
        ('REGISTER', 's2')
    ]


def test_equ(get_tokens):
    assert get_tokens('variable_name EQU 123') == [
        ('NAME', 'variable_name'),
        ('INSTRUCTION', 'EQU'),
        ('NUMBER', 123)
    ]


def test_jump_to_address(get_tokens):
    assert get_tokens('JUMP 123') == [
        ('INSTRUCTION', 'JUMP'),
        ('NUMBER', 123)
    ]


def test_jump_to_label(get_tokens):
    assert get_tokens('JUMP foo') == [
        ('INSTRUCTION', 'JUMP'),
        ('NAME', 'foo')
    ]
