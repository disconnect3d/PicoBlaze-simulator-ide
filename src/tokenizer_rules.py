# this file is used by ply.lex
from src.errors import TokenizeException
from src.mnemonics import MNEMONICS, ADD


def name(v):
    return v.__name__

tokens = (
    *[name(i) for i in MNEMONICS.values()], 'COMMA', 'REGISTER', 'LABEL', 'NUMBER', 'NAME', 'COMMENT', 'INDICATOR',
    'FLAG'
)


def generate_function_str(name):
    function_str = "def t_%s(t):\n" % name
    function_str += "    r'(?i)\\b%s\\b'\n" % name
    function_str += "    t.value = t.value.upper()\n"
    function_str += "    return t"
    return function_str

for i in MNEMONICS.values():
    exec(generate_function_str(name(i)))

t_COMMA = r','
t_NAME = r'[A-Za-z_][A-Za-z0-9_]*'


def t_REGISTER(t):
    r'(?i)\bs((1[0-5]|[0-9])|(?i)[a-f])\b'
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
    return t


def t_INDICATOR(t):
    r'(?i)(\bC\b|\bNC\b|\bZ\b|\bNZ\b)'
    t.value = t.value.upper()
    return t


def t_FLAG(t):
    r'(?i)(\bENABLE\b|\bDISABLE\b)'
    t.value = t.value.upper()
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise TokenizeException("Illegal character '%s'" % t.value[0])
