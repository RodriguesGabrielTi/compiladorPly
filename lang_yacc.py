from ply.yacc import yacc
import lang_lex
from symbol_table.scope.out_of_scope_exception import OutOfScopeException

tokens = lang_lex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

def p_program(p):
    '''program : statement
                 | funclist'''
    p[0] = ('program', p[1])


def p_program_empty(p):
    '''program : '''
    pass


def p_funclist(p):
    '''funclist : funcdef funclist_1
    '''
    p[0] = ('func-list', p[1], p[2])


def p_funclist_1(p):
    '''funclist_1 : funcdef funclist_1'''
    p[0] = ('func-list-1', p[1], p[2])


def p_funclist_1_empty(p):
    '''funclist_1 : '''
    pass

def p_funcdef(p):
    '''funcdef : DEF IDENT LPAREN paramlist RPAREN LBRACES statelist RBRACES
    '''
    p[0] = ('funcdef', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])


def p_paramlist(p):
    '''paramlist : typecast IDENT paramlist_1'''
    p[0] = ('param-list', p[1], p[2], p[3])


def p_paramlist_empty(p):
    '''paramlist : '''
    pass


def p_paramlist_1(p):
    '''paramlist_1 : COMMA typecast IDENT paramlist_1'''
    p[0] = ('param-list-1', p[1], p[2], p[3], p[4])


def p_paramlist_1_empty(p):
    '''paramlist_1 : '''
    pass


def p_statement(p):
    '''statement : vardecl SEMICOL
                   | atribstat SEMICOL
                   | printstat SEMICOL
                   | readstat SEMICOL
                   | returnstat SEMICOL
                   | ifstat SEMICOL
                   | forstat SEMICOL
                   | BREAK SEMICOL'''
    p[0] = ('statement', p[1], p[2])


def p_statement_braces(p):
    '''statement : LBRACES statelist RBRACES'''
    p[0] = ('statement', p[1], p[2], p[3])


def p_statement_semicol(p):
    '''statement : SEMICOL'''
    p[0] = ('statement', p[1])


def p_vardecl(p):
    '''vardecl : typecast IDENT arr'''
    p[0] = ('vardecl', p[1], p[2], p[3])


def p_arr(p):
    '''arr : LBRACK INTCONST RBRACK arr'''
    p[0] = ('vardecl-array', p[1], p[2], p[3], p[4])


def p_arr_empty(p):
    '''arr : '''
    pass


def p_atribstat(p):
    '''atribstat : lvalue EQUALS atribval'''
    p[0] = ('atribstat', p[1], p[2], p[3])


def p_atribval(p):
    '''atribval : expression
                  | allocexpression
                  | funccall'''
    p[0] = ('atribval', p[1])


def p_funccall(p):
    '''funccall : IDENT LPAREN paramlistcall RPAREN'''
    p[0] = ('funccall', p[1], p[2], p[3], p[4])


def p_paramlistcall(p):
    '''paramlistcall : IDENT paramlistcall_1'''
    p[0] = ('param-list-call', p[1], p[2])


def p_paramlistcall_empty(p):
    '''paramlistcall : '''
    pass

def p_paramlistcall_1(p):
    '''paramlistcall_1 : COMMA IDENT paramlistcall_1'''
    p[0] = ('param-list-call-1', p[1], p[2], p[3])


def p_paramlistcall_1_empty(p):
    '''paramlistcall_1 :'''
    pass


def p_printstat(p):
    '''printstat : PRINT expression'''
    p[0] = ('print-stat', p[1], p[2])


def p_readstat(p):
    '''readstat : READ lvalue'''
    p[0] = ('read-stat', p[1], p[2])


def p_returnstat(p):
    '''returnstat : RETURN'''
    p[0] = ('return-stat', p[1])


def p_ifstat(p):
    '''ifstat : IF LPAREN expression RPAREN statement elsestat'''
    p[0] = ('if-stat', p[1], p[2], p[3], p[4], p[5], p[6])


def p_elsestat(p):
    '''elsestat : ELSE statement'''
    p[0] = ('else-stat', p[1], p[2])


def p_elsestat_empty(p):
    '''elsestat : '''
    pass

def p_forstat(p):
    '''forstat : FOR LPAREN atribstat SEMICOL expression SEMICOL atribstat RPAREN statement'''
    p[0] = ('forstat', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])


def p_statelist(p):
    '''statelist : statement statelist'''
    p[0] = ('state-list', p[1], p[2])


def p_statelist_empty(p):
    '''statelist : '''
    pass


def p_allocexpression(p):
    '''allocexpression : NEW typecast LBRACK numexpression RBRACK numexpressionarr'''
    p[0] = ('alloc-expression', p[1], p[2], p[3], p[4], p[5], p[6])


def p_expression(p):
    '''expression : numexpression compexpr'''
    p[0] = ('expression', p[1], p[2])


def p_compexpr(p):
    '''compexpr : comp numexpression compexpr'''
    p[0] = ('comp-expr', p[1], p[2], p[3])


def p_compexpr_empty(p):
    '''compexpr : '''
    pass


def p_numexpression(p):
    '''numexpression : term numexpression_1'''
    p[0] = ('num-expression', p[1], p[2])


def p_numexpression_1(p):
    '''numexpression_1 : plusminus term numexpression_1'''
    p[0] = ('num-expression-1', p[1], p[2], p[3])


def p_numexpression_1_empty(p):
    '''numexpression_1 :'''
    pass

def p_term(p):
    '''term : unaryexpr term_1'''
    p[0] = ('term', p[1], p[2])


def p_term_1(p):
    '''term_1 : operation unaryexpr term_1'''
    p[0] = ('term-1', p[1], p[2], p[3])


def p_term_1_empty(p):
    '''term_1 : '''
    pass


def p_unaryexpr(p):
    '''unaryexpr : plusminus factor'''
    p[0] = ('unary-expr', p[1], p[2])


def p_unaryexpr_single(p):
    '''unaryexpr : factor'''
    p[0] = ('unary-expr', p[1])


def p_factor(p):
    '''factor : INTCONST
                | FLOATCONST
                | STRCONST
                | NULL
                | lvalue'''
    p[0] = ('factor', p[1])


def p_factor_paren(p):
    '''factor : LPAREN numexpression RPAREN'''
    p[0] = ('factor', p[1], p[2], p[3])


def p_lvalue(p):
    '''lvalue : IDENT numexpressionarr'''
    p[0] = ('lvalue', p[0], p[1])


def p_typecast(p):
    '''typecast : INT
                  | FLOAT
                  | STR
                  | VOID'''
    p[0] = ('typecast', p[1])


def p_operation(p):
    '''operation : TIMES
                   | DIVIDE
                   | MOD'''
    p[0] = ('operation', p[1])


def p_comp(p):
    '''comp : LT
              | GT
              | LE
              | GE
              | EQ
              | NE'''
    p[0] = ('comp', p[1])


def p_plusminus(p):
    '''plusminus : PLUS
                   | MINUS'''
    p[0] = ('plus-minus', p[1])


def p_numexpressionarr(p):
    '''numexpressionarr : LBRACK numexpression RBRACK numexpressionarr'''
    p[0] = ('num-expression-arr', p[1], p[2], p[3], p[4])


def p_numexpressionarr_empty(p):
    '''numexpressionarr : '''


# Error rule for syntax errors
def p_error(p):
    print(p)
    print("Syntax error in input!")


# Build the parser
parser = yacc()

if __name__ == '__main__':

    s = '''def func1( int A , int B )
    {
        int SM [2];
        SM [0] = A + B;
        SM [1] = B * C;
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

    lang_lex.symbol_table.program = s
    result = parser.parse(s, debug=False)

    try:
        lang_lex.symbol_table.end()
    except OutOfScopeException as e:
        lang_lex.errors.append(str(e))
    lang_lex.symbol_table.pretty_print()
    for error in lang_lex.errors:
        print(error)
    print(result)