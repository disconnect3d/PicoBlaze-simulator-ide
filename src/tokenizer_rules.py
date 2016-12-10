# this file is used by ply.lex
from .errors import TokenizeException

tokens = (
    'INSTRUCTION', 'DIRECTIVE', 'COMMA', 'REGISTER', 'LABEL', 'NUMBER', 'NAME', 'COMMENT'
)

t_COMMA = r','
t_NAME = r'[A-Za-z_][A-Za-z0-9_]*'


def t_REGISTER(t):
    r'(?i)s((1[0-5]|[0-9])|(?i)[a-f])'
    t.value = t.value.upper()
    return t


def t_DIRECTIVE(t):
    r'(?i)ORG|EQU'
    t.value = t.value.upper()
    return t


def t_INSTRUCTION(t):
    r'(?i)LOAD|STORE|FETCH|JUMP|CALL|RETI|RET|ADDC|ADD|SUBC|SUB|XOR|OR|AND|IN|OUT|EINT|DINT|COMP'
    t.value = t.value.upper()
    return t


def t_NUMBER(t):
    r'\d+|[$](?i)[0-9a-f]+'
    try:
        if t.value[0] == '$':
            t.value = int(t.value[1:], 16)
        else:
            t.value = int(t.value)
    except ValueError:
        print("ValueError this isnt a number")
        t.value = 0

    return t


def t_LABEL(t):
    r'[A-Za-z_][A-Za-z0-9_]*:'
    t.value = t.value[:-1]  # truncates ':'
    return t


def t_COMMENT(t):
    r';.*'
    pass


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise TokenizeException("Illegal character '%s'" % t.value[0])
