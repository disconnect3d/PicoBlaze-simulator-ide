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
    return p, yacc.yacc(module=p, debug=False)


@pytest.fixture(scope='function')
def parse(ply_yacc):
    parser, yacc = ply_yacc

    def _parse(input_string):
        yacc.parse(input_string, debug=False)
        return parser.instructions

    yield _parse

    # Teardown - reset parser state (e.g. instructions list)
    parser.reset_state()


@pytest.fixture(scope='function')
def parse_directive(ply_yacc):
    parser, yacc = ply_yacc

    def _parse(input_string):
        yacc.parse(input_string)
        return parser.directives

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
    assert str(parse(' ADD    s0  ,   3')[0]) == str(ADD(reg='S0', reg_or_val=3))


def test_ADD_val_com(parse):
    assert str(parse(' ADD    s0  ,   3; dupa')[0]) == str(ADD(reg='S0', reg_or_val=3))


def test_ADD_reg(parse):
    assert str(parse('ADD s2, SF')[0]) == str(ADD(reg='S2', reg_or_val='SF'))


def test_ADD_alias_1(parse, parse_directive):
    assert str(parse_directive('somename EQU s2 ; test')[0]) == str(EQU(alias='somename', reg_or_val='S2'))
    assert str(parse('ADD somename, SF; ADD S2, SF')[0]) == str(ADD(reg='S2', reg_or_val='SF'))


def test_ADD_alias_2(parse, parse_directive):
    assert str(parse_directive('somename EQU sF')[0]) == str(EQU(alias='somename', reg_or_val='SF'))
    assert str(parse('ADD s2, somename')[0]) == str(ADD(reg='S2', reg_or_val='SF'))


def test_ADD_alias_1_2(parse, parse_directive):
    assert str(parse_directive('name1 EQU sF')[0]) == str(EQU(alias='name1', reg_or_val='SF'))
    assert str(parse_directive('name2 EQU 5')[1]) == str(EQU(alias='name2', reg_or_val=5))
    assert str(parse('ADD name1, name2')[0]) == str(ADD(reg='SF', reg_or_val=5))


def test_ADDC_val(parse):
    assert str(parse(' ADDC s0, 3')[0]) == str(ADDC(reg='S0', reg_or_val=3))


def test_ADDC_reg(parse):
    assert str(parse('ADDC S2, sf')[0]) == str(ADDC(reg='S2', reg_or_val='SF'))


def test_AND_val(parse):
    assert str(parse('AND s0, 3')[0]) == str(AND(reg='S0', reg_or_val=3))


def test_AND_reg(parse):
    assert str(parse('and S2, sf')[0]) == str(AND(reg='S2', reg_or_val='SF'))


def test_COMP_val(parse):
    assert str(parse('comp s0, 3')[0]) == str(COMP(reg='S0', reg_or_val=3))


def test_COMP_reg(parse):
    assert str(parse('comP S2, sf')[0]) == str(COMP(reg='S2', reg_or_val='SF'))


def test_FETCH_val(parse):
    assert str(parse('Fetch s0, 3')[0]) == str(FETCH(reg='S0', reg_or_val=3))


def test_FETCH_reg(parse):
    assert str(parse('FETCH S2, sf')[0]) == str(FETCH(reg='S2', reg_or_val='SF'))


def test_IN_val(parse):
    assert str(parse('in s0, 3')[0]) == str(IN(reg='S0', reg_or_val=3))


def test_IN_reg(parse):
    assert str(parse('In S2, sf')[0]) == str(IN(reg='S2', reg_or_val='SF'))


def test_LOAD_val(parse):
    assert str(parse('load s0, 3')[0]) == str(LOAD(reg='S0', reg_or_val=3))


def test_LOAD_reg(parse):
    assert str(parse('LOAD S2, sf')[0]) == str(LOAD(reg='S2', reg_or_val='SF'))


def test_OR_val(parse):
    assert str(parse('or s0, 3')[0]) == str(OR(reg='S0', reg_or_val=3))


def test_OR_reg(parse):
    assert str(parse('Or S2, sf')[0]) == str(OR(reg='S2', reg_or_val='SF'))


def test_OUT_val(parse):
    assert str(parse('out s0, 3')[0]) == str(OUT(reg='S0', reg_or_val=3))


def test_OUT_reg(parse):
    assert parse('OUT S2, sf')[0] == OUT(reg='S2', reg_or_val='SF')


def test_STORE_val(parse):
    assert parse('store s0, 3')[0] == STORE(reg='S0', reg_or_val=3)


def test_STORE_reg(parse):
    assert parse('STORE S2, sf')[0] == STORE(reg='S2', reg_or_val='SF')


def test_SUB_val(parse):
    assert parse('sub s0, 3')[0] == SUB(reg='S0', reg_or_val=3)


def test_SUB_reg(parse):
    assert parse('SUB S2, sf')[0] == SUB(reg='S2', reg_or_val='SF')


def test_SUBC_val(parse):
    assert parse('subc s0, 3')[0] == SUBC(reg='S0', reg_or_val=3)


def test_SUBC_reg(parse):
    assert parse('SuBc s2, S3')[0] == SUBC(reg='S2', reg_or_val='S3')


def test_TEST_val(parse):
    assert parse('test s0, 3')[0] == TEST(reg='S0', reg_or_val=3)


def test_TEST_reg(parse):
    assert parse('TEST s2, S3')[0] == TEST(reg='S2', reg_or_val='S3')


def test_XOR_val(parse):
    assert parse('xor s0, 3')[0] == XOR(reg='S0', reg_or_val=3)


def test_XOR_reg(parse):
    assert parse('XOR s2, S3')[0] == XOR(reg='S2', reg_or_val='S3')


def test_CALL(parse):
    assert parse('CALL place')[0] == CALL(label_or_ind='place', label_or_addr=None)


def test_CALL_ind(parse):
    assert parse('call Nz, place')[0] == CALL(label_or_ind='NZ', label_or_addr='place')


def test_CALL_addr(parse):
    assert parse('call Nz, $3FF')[0] == CALL(label_or_ind='NZ', label_or_addr=1023)


def test_JUMP(parse):
    assert parse('jump place')[0] == JUMP(label_or_ind='place', label_or_addr=None)


def test_JUMP_ind(parse):
    assert parse('JUMP Z, place')[0] == JUMP(label_or_ind='Z', label_or_addr='place')


def test_JUMP_addr(parse):
    assert parse('JUMP Z, $3FF')[0] == JUMP(label_or_ind='Z', label_or_addr=1023)


def test_RET(parse):
    assert parse('ret')[0] == RET(indicator=None)


def test_RET_ind(parse):
    assert parse('RET C')[0] == RET(indicator='C')


def test_DINT(parse):
    assert parse('DINT')[0] == DINT()


def test_EINT(parse):
    assert parse('EINT')[0] == EINT()


def test_RETI_enable(parse):
    assert parse('RETI ENABLE')[0] == RETI(flag='ENABLE')


def test_RETI_disable(parse):
    assert parse('reti disable')[0] == RETI(flag='DISABLE')


def test_RL(parse):
    assert parse('RL s1')[0] == RL(reg='S1')


def test_RR(parse):
    assert parse('RR s1')[0] == RR(reg='S1')


def test_SL0(parse):
    assert parse('sl0 s1')[0] == SL0(reg='S1')


def test_SL1(parse):
    assert parse('SL1 s1')[0] == SL1(reg='S1')


def test_SLA(parse):
    assert parse('SLA se')[0] == SLA(reg='SE')


def test_SLX(parse):
    assert parse('SLX se')[0] == SLX(reg='SE')


def test_SR0(parse):
    assert parse('sr0 s1')[0] == SR0(reg='S1')


def test_SR1(parse):
    assert parse('SR1 s1')[0] == SR1(reg='S1')


def test_SRA(parse):
    assert parse('SRA se')[0] == SRA(reg='SE')


def test_SRX(parse):
    assert str(parse('SRX se')[0]) == str(SRX(reg='SE'))


def test_label(parse):
    assert str(parse('loop:')[0]) == str(LABEL(alias='loop'))


def test_label_with_instruction(parse):
    # print(parse('sleep_loop: SUB s0, 1'))
    assert [str(i) for i in parse('sleep_loop: SUB s0, 1')] == [
        str(LABEL(alias='sleep_loop')),
        str(SUB(reg='S0', reg_or_val=1)),
    ]


def test_EQU_val(parse_directive):
    assert str(parse_directive('variable_name EQU 10')[0]) == str(EQU(alias='variable_name', reg_or_val=10))


def test_EQU_reg(parse_directive):
    assert str(parse_directive('reg_name EQU s5')[0]) == str(EQU(alias='reg_name', reg_or_val='S5'))


def test_ORG(parse):
    assert str(parse('ORG $3ff')[0]) == str(ORG(addr=0x3ff))


def test_DSIN(parse_directive):
    assert str(parse_directive('input DSIN 45')[0]) == str(DSIN(alias='input', pp=45))


def test_DSOUT(parse_directive):
    assert str(parse_directive('output dsout 45')[0]) == str(DSOUT(alias='output', pp=45))


def test_DSIO(parse_directive):
    assert str(parse_directive('io DsIO 45')[0]) == str(DSIO(alias='io', pp=45))


def test_comment(parse):
    assert parse(';s1 add s5 equ sf') == []
