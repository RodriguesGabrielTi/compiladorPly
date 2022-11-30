from ply.yacc import yacc
import lang_lex

tokens = lang_lex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

def p_program(p):
    '''program : statement
            | funclist
            |'''
    pass


def p_funclist(p):
    '''funclist : funcdef funclist
                | funcdef
    '''
    pass


def p_funcdef(p):
    '''funcdef : DEF IDENT RPAREN paramlist LPAREN RBRACES statelist LBRACES
    '''
    pass


def p_paramlist(p):
    '''paramlist : paramlist0
                 |'''
    pass


def p_paramlist0(p):
    '''paramlist0 : INT IDENT COMMA paramlist0
                  | FLOAT IDENT COMMA paramlist0
                  | STR IDENT COMMA paramlist0
                  | INT IDENT
                  | FLOAT IDENT
                  | STR IDENT'''
    pass


def p_statement(p):
    '''statement : vardecl SEMICOL
                 | atribstat SEMICOL
                 | printstat SEMICOL
                 | readstat SEMICOL
                 | returnstat SEMICOL
                 | ifstat SEMICOL
                 | forstat SEMICOL
                 | RBRACES statelist LBRACES
                 | break SEMICOL
                 | SEMICOL'''
    pass


def p_vardecl(p):
    '''vardecl : INT IDENT array
               | FLOAT IDENT array
               | STR IDENT array'''
    pass

def p_array(p):
    '''array : RBRACK INTCONST LBRACK array
             |'''
    pass


def p_atribstat(p):
    '''atribstat : lvalue EQUALS expression
                 | lvalue EQUALS allocexpression
                 | lvalue EQUALS funccall'''
    pass


def p_funccal(p):
    '''funccal : IDENT RPAREN paramlistcall LPAREN'''
    pass


def p_paramlistcall(p):
    '''paramlistcall : paramlistcall0
                    |'''
    pass


def p_paramlistcall0(p):
    '''paramlistcall0 : IDENT COMMA paramlistcall0
                     | IDENT'''
    pass


def p_printstat(p):
    '''printstat : PRINT expression'''
    pass


def p_readstat(p):
    '''readstat : READ lvalue'''
    pass


def p_returnstat(p):
    '''returnstat : RETURN'''
    pass


def p_ifstat(p):
    '''ifstat : IF RPAREN expression LPAREN statement
              | IF RPAREN expression LPAREN statement ELSE statement'''
    pass


def p_forstat(p):
    '''forstat : FOR RPAREN atribstat SEMICOL expression SEMICOL atribstat LPAREN STATEMENT'''
    pass


def p_statelist(p):
    '''statelist : statement
                 | statement statelist'''
    pass


def p_allocexpression(p):
    '''allocexpression : NEW INT numexpressionlist
                       | NEW FLOAT numexpressionlist
                       | NEW STRING numexpressionlist'''
    pass


def p_numexpressionlist(p):
    '''numexpressionlist : RBRACK numexpression LBRACK numexpressionlist
                         |'''
    pass


def p_expression(p):
    pass


def p_numexpression(p):
    pass


def p_term(p):
    pass


def p_unaryexpr(p):
    pass


def p_factor(p):
    pass


def p_lvalues(p):
    pass