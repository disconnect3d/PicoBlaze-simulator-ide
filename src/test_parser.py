import pytest
from ply import lex, yacc

import src.tokenizer_rules as tokenizer_rules
from src.errors import ParseException
from src.mnemonics import *
from src.parser_rules import Parser


@pytest.fixture(scope='session')
def ply_yacc():
    p = Parser()

    lex.lex(module=tokenizer_rules)

    # As we need to store state in the parser (parsed instructions list) we need to make an ugly hack
    # of passing the parser as a module because the yacc.yacc wasn't design to hold the state in the parser
    p.tokens = tokenizer_rules.tokens
    return p, yacc.yacc(module=p)

ply_yacc()


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


# namedtuples are equal even if they have different names but same content, so we need workaround:
# checking string representation
def test_ADD_val(parse):
    assert parse(' ADD    s0  ,   3')[0].__str__() == ADD(reg='S0', reg_or_val=3).__str__()


def test_ADD_reg(parse):
    assert parse('ADD s2, SF')[0].__str__() == ADD(reg='S2', reg_or_val='SF').__str__()


def test_ADDC_val(parse):
    assert parse(' ADDC s0, 3')[0].__str__() == ADDC(reg='S0', reg_or_val=3).__str__()


def test_ADDC_reg(parse):
    assert parse('ADDC S2, sf')[0].__str__() == ADDC(reg='S2', reg_or_val='SF').__str__()


def test_AND_val(parse):
    assert parse('AND s0, 3')[0].__str__() == AND(reg='S0', reg_or_val=3).__str__()


def test_AND_reg(parse):
    assert parse('and S2, sf')[0].__str__() == AND(reg='S2', reg_or_val='SF').__str__()


def test_COMP_val(parse):
    assert parse('comp s0, 3')[0].__str__() == COMP(reg='S0', reg_or_val=3).__str__()


def test_COMP_reg(parse):
    assert parse('comP S2, sf')[0].__str__() == COMP(reg='S2', reg_or_val='SF').__str__()


def test_FETCH_val(parse):
    assert parse('Fetch s0, 3')[0].__str__() == FETCH(reg='S0', reg_or_val=3).__str__()


def test_FETCH_reg(parse):
    assert parse('FETCH S2, sf')[0].__str__() == FETCH(reg='S2', reg_or_val='SF').__str__()


def test_IN_val(parse):
    assert parse('in s0, 3')[0].__str__() == IN(reg='S0', reg_or_val=3).__str__()


def test_IN_reg(parse):
    assert parse('In S2, sf')[0].__str__() == IN(reg='S2', reg_or_val='SF').__str__()


def test_LOAD_val(parse):
    assert parse('load s0, 3')[0].__str__() == LOAD(reg='S0', reg_or_val=3).__str__()


def test_LOAD_reg(parse):
    assert parse('LOAD S2, sf')[0].__str__() == LOAD(reg='S2', reg_or_val='SF').__str__()


def test_OR_val(parse):
    assert parse('or s0, 3')[0].__str__() == OR(reg='S0', reg_or_val=3).__str__()


def test_OR_reg(parse):
    assert parse('Or S2, sf')[0].__str__() == OR(reg='S2', reg_or_val='SF').__str__()


def test_OUT_val(parse):
    assert parse('out s0, 3')[0].__str__() == OUT(reg='S0', reg_or_val=3).__str__()


def test_OUT_reg(parse):
    assert parse('OUT S2, sf')[0].__str__() == OUT(reg='S2', reg_or_val='SF').__str__()


def test_STORE_val(parse):
    assert parse('store s0, 3')[0].__str__() == STORE(reg='S0', reg_or_val=3).__str__()


def test_STORE_reg(parse):
    assert parse('STORE S2, sf')[0].__str__() == STORE(reg='S2', reg_or_val='SF').__str__()


def test_SUB_val(parse):
    assert parse('sub s0, 3')[0].__str__() == SUB(reg='S0', reg_or_val=3).__str__()


def test_SUB_reg(parse):
    assert parse('SUB S2, sf')[0].__str__() == SUB(reg='S2', reg_or_val='SF').__str__()


def test_SUBC_val(parse):
    assert parse('subc s0, 3')[0].__str__() == SUBC(reg='S0', reg_or_val=3).__str__()


def test_SUBC_reg(parse):
    assert parse('SuBc s2, S3')[0].__str__() == SUBC(reg='S2', reg_or_val='S3').__str__()


def test_TEST_val(parse):
    assert parse('test s0, 3')[0].__str__() == TEST(reg='S0', reg_or_val=3).__str__()


def test_TEST_reg(parse):
    assert parse('TEST s2, S3')[0].__str__() == TEST(reg='S2', reg_or_val='S3').__str__()


def test_XOR_val(parse):
    assert parse('xor s0, 3')[0].__str__() == XOR(reg='S0', reg_or_val=3).__str__()


def test_XOR_reg(parse):
    assert parse('XOR s2, S3')[0].__str__() == XOR(reg='S2', reg_or_val='S3').__str__()


def test_CALL(parse):
    assert parse('CALL place')[0].__str__() == CALL(label_or_ind='place', label=None).__str__()


def test_CALL_ind(parse):
    assert parse('call Nz, place')[0].__str__() == CALL(label_or_ind='NZ', label='place').__str__()


def test_JUMP(parse):
    assert parse('jump place')[0].__str__() == JUMP(label_or_ind='place', label=None).__str__()


def test_JUMP_ind(parse):
    assert parse('JUMP Z, place')[0].__str__() == JUMP(label_or_ind='Z', label='place').__str__()


def test_RET(parse):
    assert parse('ret')[0].__str__() == RET(indicator=None).__str__()


def test_RET_ind(parse):
    assert parse('RET C')[0].__str__() == RET(indicator='C').__str__()


def test_DINT(parse):
    assert parse('DINT')[0].__str__() == DINT().__str__()


def test_EINT(parse):
    assert parse('EINT')[0].__str__() == EINT().__str__()


def test_RETI_enable(parse):
    assert parse('RETI ENABLE')[0].__str__() == RETI(flag='ENABLE').__str__()


def test_RETI_disable(parse):
    assert parse('reti disable')[0].__str__() == RETI(flag='DISABLE').__str__()


def test_RL(parse):
    assert parse('RL s1')[0].__str__() == RL(reg='S1').__str__()


def test_RR(parse):
    assert parse('RR s1')[0].__str__() == RR(reg='S1').__str__()


def test_SL0(parse):
    assert parse('sl0 s1')[0].__str__() == SL0(reg='S1').__str__()


def test_SL1(parse):
    assert parse('SL1 s1')[0].__str__() == SL1(reg='S1').__str__()


def test_SLA(parse):
    assert parse('SLA se')[0].__str__() == SLA(reg='SE').__str__()


def test_SLX(parse):
    assert parse('SLX se')[0].__str__() == SLX(reg='SE').__str__()


def test_SR0(parse):
    assert parse('sr0 s1')[0].__str__() == SR0(reg='S1').__str__()


def test_SR1(parse):
    assert parse('SR1 s1')[0].__str__() == SR1(reg='S1').__str__()


def test_SRA(parse):
    assert parse('SRA se')[0].__str__() == SRA(reg='SE').__str__()


def test_SRX(parse):
    assert parse('SRX se')[0].__str__() == SRX(reg='SE').__str__()


def test_label(parse):
    assert parse('loop:')[0].__str__() == LABEL(alias='loop').__str__()


def test_label_with_instruction(parse):
    assert [i.__str__() for i in parse('sleep_loop: SUB s0, 1')] == [
        LABEL(alias='sleep_loop').__str__(),
        SUB(reg='S0', reg_or_val=1).__str__()
    ]


def test_EQU_val(parse):
    assert parse('variable_name EQU 10')[0].__str__() == EQU(alias='variable_name', reg_or_val=10).__str__()


def test_EQU_reg(parse):
    assert parse('reg_name EQU s5')[0].__str__() == EQU(alias='reg_name', reg_or_val='S5').__str__()


def test_ORG(parse):
    assert parse('ORG $3ff')[0].__str__() == ORG(addr=0x3ff).__str__()


def test_DSIN(parse):
    assert parse('input DSIN 45')[0].__str__() == DSIN(alias='input', pp=45).__str__()


def test_DSOUT(parse):
    assert parse('output dsout 45')[0].__str__() == DSOUT(alias='output', pp=45).__str__()


def test_DSIO(parse):
    assert parse('io DsIO 45')[0].__str__() == DSIO(alias='io', pp=45).__str__()


def test_comment(parse):
    assert parse(';s1 add s5 equ sf') == []



