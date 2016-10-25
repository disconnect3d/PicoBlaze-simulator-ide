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
        ('NAME', 'LOAD'),
        ('REGISTER', 's0'),
        ('COMMA', ','),
        ('NUMBER', 123)
    ]


def test_add(get_tokens):
    assert get_tokens('ADD s5, 23') == [
        ('NAME', 'ADD'),
        ('REGISTER', 's5'),
        ('COMMA', ','),
        ('NUMBER', 23)
    ]


def test_equ(get_tokens):
    assert get_tokens('a EQU 123') == [
        ('NAME', 'a'),
        ('NAME', 'EQU'),
        ('NUMBER', 123)
    ]


def test_jump_to_address(get_tokens):
    assert get_tokens('JUMP 123') == [
        ('NAME', 'JUMP'),
        ('NUMBER', 123)
    ]


def test_jump_to_label(get_tokens):
    assert get_tokens('JUMP foo') == [
        ('NAME', 'JUMP'),
        ('NAME', 'foo')
    ]
