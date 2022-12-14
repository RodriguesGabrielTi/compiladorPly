from ply.lex import lex

from symbol_table.scope.out_of_scope_exception import OutOfScopeException
from symbol_table.symbol import Symbol, Occurrence, TokenSuperType
from symbol_table.symbol_table import SymbolTable


errors: list[str] = []


def create_symbol_entry(t, super_type: TokenSuperType):
    new_symbol = Symbol(t.type, super_type, t.value)
    line = t.lexer.lineno
    column = find_column(symbol_table.program, t)
    occurrence = Occurrence(line, column)
    try:
        symbol_table.add_symbol(new_symbol, occurrence)
    except OutOfScopeException as e:
        errors.append(str(e))
        t.lexer.skip(1)


# --- Symbol Table
symbol_table = SymbolTable()

# --- TOKENIZER

# PALAVRAS RESERVADAS
reserved = {'def': 'DEF',
            'void': 'VOID',
            'int': 'INT',
            'float': 'FLOAT',
            'str': 'STR',
            'return': 'RETURN',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'for': 'FOR',
            'print': 'PRINT',
            'read': 'READ',
            'new': 'NEW',
            'break': 'BREAK',
            'null': 'NULL',
            'exec': 'EXEC'}

tokens = list(reserved.values()) + ['RPAREN', 'LPAREN', 'RBRACES', 'LBRACES', 'RBRACK', 'LBRACK',
                                    'COMMA', 'SEMICOL', 'COLON',
                                    'EQUALS', 'MINUS', 'PLUS', 'TIMES', 'POT', 'DIVIDE', 'MOD', 'OR', 'AND',
                                    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
                                    'COMMENT',
                                    'IDENT', 'STRCONST', 'INTCONST', 'FLOATCONST']

# Ignora Espaços e Tabs
t_ignore = ' \t'


# DELIMITADORES
def t_RPAREN(t):
    r'\)'
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_LPAREN(t):
    r'\('
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_RBRACES(t):
    r'\}'
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_LBRACES(t):
    r'\{'
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_RBRACK(t):
    r'\]'
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_LBRACK(t):
    r'\['
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


# PONTUAÇÃO
def t_COMMA(t):
    r','
    create_symbol_entry(t, TokenSuperType.PUNCTUATION)
    return t


def t_SEMICOL(t):
    r';'
    create_symbol_entry(t, TokenSuperType.PUNCTUATION)
    return t


def t_COLON(t):
    r':'
    create_symbol_entry(t, TokenSuperType.PUNCTUATION)
    return t


# OPERAÇÕES
def t_EQUALS(t):
    r'='
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_MINUS(t):
    r'-'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_PLUS(t):
    r'\+'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_TIMES(t):
    r'\*'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_POT(t):
    r'\^'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_DIVIDE(t):
    r'/'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_MOD(t):
    r'%'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_OR(t):
    r'\|\|'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_AND(t):
    r'&&'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_LT(t):
    r'<'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_GT(t):
    r'>'
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_LE(t):
    r'<='
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t

def t_GE(t):
    r'>='
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_EQ(t):
    r'=='
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


def t_NE(t):
    r'!='
    create_symbol_entry(t, TokenSuperType.OPERATION)
    return t


# SIMBOLOS NÃO TRIVIAIS
def t_STRCONST(t):
    r'([\"][^\"]*[\"])'
    create_symbol_entry(t, TokenSuperType.NON_TRIVIAL)
    return t


def t_IDENT(t):
    r'[a-zA-Z]([a-zA-Z]|[\d]|[\_])*'
    t.type = reserved.get(t.value, 'IDENT')
    if t.type == 'IDENT':
        supertype = TokenSuperType.NON_TRIVIAL
    else:
        supertype = TokenSuperType.RESERVED_WORD
    create_symbol_entry(t, supertype)
    return t


def t_INTCONST(t):
    r'(\+|-)?\d+'
    t.value = int(t.value)
    create_symbol_entry(t, TokenSuperType.NON_TRIVIAL)
    return t


def t_FLOATCONST(t):
    r'(\+|-)?[\d]+([\.])?[\d]+'
    t.value = float(t.value)
    create_symbol_entry(t, TokenSuperType.NON_TRIVIAL)
    return t


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    create_symbol_entry(t, TokenSuperType.NON_TRIVIAL)
    t.lexer.lineno += t.value.count('\n')


# Error handler for illegal characters
def t_error(t):
    errors.append(f'Palavra inválida {t.value[0]!r} \n'
          f'linha: {t.lexer.lineno} \n'
          f'coluna: {find_column(symbol_table.program, t)} ')
    t.lexer.skip(1)


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(data, token):
    line_start = data.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def read_files():
    codes = []
    paths = ["kruskal.lcc"]
    for path in paths:
        with open(path, 'r') as file:
            codes.append((path, file.read()))
    return codes


lexer = lex()
if __name__ == "__main__":
    codes = read_files()
    for code in codes:
        file_name = code[0]
        print(f"CODE: {file_name}")
        symbol_table.program = code[1]

        # Give the lexer some input
        lexer.input(code[1])
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
        try:
            symbol_table.end()
        except OutOfScopeException as e:
            errors.append(str(e))
        symbol_table.pretty_print()
        for error in errors:
            print(error)
