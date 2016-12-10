import pytest
from ply import lex, yacc

import src.tokenizer_rules as tokenizer_rules
from src.errors import ParseException
from src.mnemonics import EQU1, ORG, LABEL, SUB1
from src.parser_rules import Parser


@pytest.fixture(scope='session')
def ply_yacc():
    p = Parser()

    lex.lex(module=tokenizer_rules)

    # As we need to store state in the parser (parsed instructions list) we need to make an ugly hack
    # of passing the parser as a module because the yacc.yacc wasn't design to hold the state in the parser
    p.tokens = tokenizer_rules.tokens
    return p, yacc.yacc(module=p)


@pytest.fixture(scope='function')
def parse(ply_yacc):
    parser, yacc = ply_yacc

    def _parse(input_string):
        yacc.parse(input_string)
        return parser.instructions

    yield _parse

    # Teardown - reset parser state (e.g. instructions list)
    parser.reset_state()


def test_bad_parsing(parse):
    for bad_code in ('$123', '10', '$123', 'ADD asd:', 'label: EQU'):
        with pytest.raises(ParseException):
            parse(bad_code)


def test_equ_directive(parse):
    assert parse('variable_name EQU 10') == [EQU1(alias='variable_name', arg=10)]


def test_org_directive(parse):
    assert parse('ORG $3ff') == [ORG(addr=0x3ff)]


def test_label(parse):
    assert parse('loop:') == [LABEL(alias='loop')]


def test_label_with_instruction(parse):
    assert parse('sleep_loop: SUB s0, 1') == [
        LABEL(alias='sleep_loop'),
        SUB1(reg='S0', arg=1)
    ]