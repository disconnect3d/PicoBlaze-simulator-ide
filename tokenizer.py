
tokens = (
    'LOAD', 'ADD', 'JUMP', 'EQU', 'COMMENT',
    'NAME', 'LABEL', 'NUMBER',
)

# Instructions
t_LOAD = r'LOAD'
t_ADD = r'ADD'
t_JUMP = r'JUMP'
t_EQU = r'EQU'

# Other tokens
t_NAME = r'[A-Za-z][A-Za-z0-9]*'
t_LABEL = r'[A-Za-z][A-Za-z0-9]*:'


def t_NUMBER(t):
    r'\d+'

    try:
        t.value = int(t.value)
    except ValueError:
        print("ValueError this isnt a number")
        t.value = 0

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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
