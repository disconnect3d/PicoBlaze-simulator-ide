import pytest
from src.virtual_machine import VirtualMachine
from os import remove


@pytest.fixture(scope='session')
def create_and_parse():

    def _create_and_parse(orders):
        lines = map(lambda x: x + '\n', orders)
        with open('testfile', 'w') as file:
            file.writelines(lines)

        vm = VirtualMachine()
        vm.parse_file('testfile')
        return vm

    yield _create_and_parse
    remove('testfile')


def test1(create_and_parse):
    vm = create_and_parse(['LOAD s0, 5', 'ADD s0, 1'])
    vm.step_many(2)
    assert vm.registers['S0'] == 6


def test2(create_and_parse):
    with pytest.raises(RuntimeError):
        vm = create_and_parse(['LOAD sF, 7'])
        vm.step_many(1025)


def test3(create_and_parse):
    with pytest.raises(RuntimeError):
        vm = create_and_parse(['reg1 EQU s0',
                               'num1 EQU 6',
                               'LOAD reg1, 5',
                               'CALL NZ, $3FF',
                               'ORG $3FF',
                               'ADD reg1, num1'])
        vm.step_over()
        assert vm.registers['S0'] == 5
        vm.step_over()
        assert vm._stack == [1]
        vm.step_over()
        assert vm.registers['S0'] == 11
        vm.step_over()


def test4(create_and_parse):
    vm = create_and_parse(['LOAD s2, 128',
                           'SL0 s2',
                           'JUMP Z, 42',
                           'ORG 35',
                           'RET',
                           'ORG 42',
                           'CALL C, 35'])
    vm.step_many(2)
    assert vm._zero == 1
    assert vm._carry == 1
    vm.step_over()
    assert vm._program_cnt == 42
    vm.step_over()
    assert vm._stack == [42]
    assert vm._program_cnt == 35
    vm.step_over()
    assert vm._stack == []
    assert vm._program_cnt == 43
