from typing import List

from ply.lex import lex

from symbol_table.scope.out_of_scope_exception import OutOfScopeException
from symbol_table.symbol import Symbol, Occurrence, TokenSuperType
from symbol_table.symbol_table import SymbolTable


errors: List[str] = []


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

# Token
tokens = list(reserved.values()) + ['RPAREN', 'LPAREN', 'RBRACES', 'LBRACES', 'RBRACK', 'LBRACK',
                                    'COMMA', 'SEMICOL', 'COLON',
                                    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
                                    'EQUALS', 'MINUS', 'PLUS', 'TIMES', 'DIVIDE', 'MOD', 'OR', 'AND',
                                    'COMMENT',
                                    'IDENT', 'STRCONST', 'INTCONST', 'FLOATCONST']

# Ignora Espaços e Tabs
t_ignore = ' \t'


# Line comment
def t_COMMENT(t):
    r'(//.*?(\n|$))'
    t.lexer.lineno += t.value.count('\n')


# DELIMITADORES
def t_RPAREN(t):
    r'\)'
    # Calculo de escopo
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_LPAREN(t):
    r'\('
    # Calculo de escopo
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_RBRACES(t):
    r'\}'
    # Calculo de escopo
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_LBRACES(t):
    r'\{'
    # Calculo de escopo
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_RBRACK(t):
    r'\]'
    # Calculo de escopo
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


def t_LBRACK(t):
    r'\['
    # Calculo de escopo
    create_symbol_entry(t, TokenSuperType.DELIMITER)
    return t


# PONTUAÇÃO
def t_COMMA(t):
    r','
    return t


def t_SEMICOL(t):
    r';'
    return t


def t_COLON(t):
    r':'
    return t


# OPERAÇÕES
def t_OR(t):
    r'\|\|'
    return t


def t_AND(t):
    r'&&'
    return t


def t_LE(t):
    r'<='
    return t


def t_GE(t):
    r'>='
    return t

def t_EQ(t):
    r'=='
    return t


def t_NE(t):
    r'!='
    return t


def t_EQUALS(t):
    r'='
    return t


def t_MINUS(t):
    r'-'
    return t


def t_PLUS(t):
    r'\+'
    return t


def t_TIMES(t):
    r'\*'
    return t


def t_DIVIDE(t):
    r'/'
    return t


def t_MOD(t):
    r'%'
    return t


def t_LT(t):
    r'<'
    return t


def t_GT(t):
    r'>'
    return t


# SIMBOLOS NÃO TRIVIAIS
def t_STRCONST(t):
    r'([\"][^\"]*[\"])'
    return t


def t_IDENT(t):
    r'[a-zA-Z]([a-zA-Z]|[\d]|[\_])*'
    t.type = reserved.get(t.value, 'IDENT')
    if t.type == 'IDENT':
        # Adiciona na tabela de símbolos
        create_symbol_entry(t, TokenSuperType.NON_TRIVIAL)
    return t


def t_INTCONST(t):
    r'(\+|-)?\d+'
    t.value = int(t.value)
    return t


def t_FLOATCONST(t):
    r'(\+|-)?[\d]+([\.])?[\d]+'
    t.value = float(t.value)
    return t


# Ignora quebras de linha
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


# Erro para palavras ilegais
def t_error(t):
    errors.append(f'Palavra inválida {t.value[0]!r} \n'
          f'linha: {t.lexer.lineno} \n'
          f'coluna: {find_column(symbol_table.program, t)} ')
    t.lexer.skip(1)


# Calcula a coluna com base na posição do token e a linha atual
def find_column(data, token):
    line_start = data.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def read_files():
    codes = []
    paths = ["formulas.lcc"]
    for path in paths:
        with open(path, 'r') as file:
            codes.append((path, file.read()))
    return codes


lexer = lex()
