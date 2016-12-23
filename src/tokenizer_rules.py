# this file is used by ply.lex
from src.errors import TokenizeException
from src.mnemonics import MNEMONICS

tokens = (
    *[i.__name__ for i in MNEMONICS.values()], 'COMMA', 'REGISTER', 'LABEL', 'NUMBER', 'NAME', 'COMMENT'
)

for i in MNEMONICS.values():
    exec("def t_%s(t):\n    r'(?i)\\b%s\\b'\n    t.value = t.value.upper()\n    return t" % (i.__name__, i.__name__))

t_COMMA = r','
t_NAME = r'[A-Za-z_][A-Za-z0-9_]*'

def t_REGISTER(t):
    r'(?i)s((1[0-5]|[0-9])|(?i)[a-f])'
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
