from ply.lex import lex

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
            'for': 'FOR',
            'print': 'PRINT',
            'read': 'READ'}

tokens = list(reserved.values()) + ['RPAREN', 'LPAREN', 'RBRACES', 'LBRACES', 'RBRACK', 'LBRACK',
                     'COMMA', 'SEMICOL', 'COLON',
                     'EQUALS', 'MINUS', 'PLUS', 'TIMES', 'DIVIDE', 'OR', 'AND', 'NOT', 'LT', 'LE', 'GT', 'GE', 'EQ',
                     'NE',
                     'COMMENT',
                     'IDENT', 'STRCONST', 'INTCONST', 'FLOATCONST']

# Ignora Espaços e Tabs
t_ignore = ' \t'

# DELIMITADORES
t_RPAREN = r'\('
t_LPAREN = r'\)'
t_RBRACES = r'\{'
t_LBRACES = r'\}'
t_RBRACK = r'\['
t_LBRACK = r'\]'

# PONTUAÇÃO
t_COMMA = r','
t_SEMICOL = r';'
t_COLON = r':'

# OPERAÇÕES
t_EQUALS = r'='
t_MINUS = r'-'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# SIMBOLOS NÃO TRIVIAIS
t_STRCONST = r'([\"][^\"]*[\"])'


def t_IDENT(t):
    r'[a-zA-Z]([a-zA-Z]|[\d]|[\_])*'
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_INTCONST(t):
    r'(\+|-)?\d+'
    t.value = int(t.value)
    return t


def t_FLOATCONST(t):
    r'(\+|-)?[\d]+([\.])?[\d]+'
    t.value = float(t.value)
    return t


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)


# Build the lexer object
lexer = lex()
if __name__ == "__main__":
    # lex.runmain(lexer)

    # Teste exemplo do professor
    data = '''
    def func1( int A , int B )
    {
        int SM [2];
        SM [0] = A + B ;
        SM [1] = B * C ;
        return;
    }
    def principal()
    {
    int C;
    int D;
    int R;
    C = 4;
    D = 5;
    R = func1 (C , D );
    return;
    }
    '''

    # Give the lexer some input
    lexer.input(data)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
