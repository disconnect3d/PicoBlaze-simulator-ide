import pytest
from parser_rules import Parser
from ply import lex, yacc

import tokenizer_rules
from tokenizer_rules import tokens


@pytest.fixture(scope='session')
def parser():
    # Ugly hack because the yacc parser itself can't be passed as an object...
    # So instead we pass it as module and just add there the tokens.
    p = Parser()
    p.tokens = tokens
    return p


@pytest.fixture(scope='session')
def ply_yacc(parser):
    lex.lex(module=tokenizer_rules)
    return yacc.yacc(module=parser)


@pytest.fixture(scope='session')
def parse(ply_yacc, parser):
    def _parse(input_string):
        ply_yacc.parse(input_string)
        return parser.instructions

    return _parse


def test_equ(parse):
    assert parse("variable_name EQU 10") == []


