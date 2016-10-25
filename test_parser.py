import pytest
from ply import lex, yacc


import tokenizer_rules
from parser_rules import Parser
from tokenizer_rules import tokens


@pytest.fixture(scope='session')
def parser():
    # Ugly hack because the yacc parser itself can't be passed as an object...
    # So instead we pass it as module and just add there the tokens.
    p = Parser()
    p.tokens = tokens
    lex.lex(module=tokenizer_rules)
    return yacc.yacc(module=p)


@pytest.fixture(scope='session')
def parse(parser):
    def _parse(input_string):
        parser.parse(input_string)
        return parser

    return _parse


def test_equ(parse):
    assert parse("variable_name EQU 10") == []


