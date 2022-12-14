from symbol_table.scope.scope import Scope, ScopeSymbol

from symbol_table.scope.out_of_scope_exception import OutOfScopeException


def get_scope_symbol_from_token(token_type: str):
    if token_type in ['LBRACES', 'RBRACES']:
        return ScopeSymbol.BRACE
    if token_type in ['LBRACK', 'RBRACK']:
        return ScopeSymbol.BRACK
    if token_type in ['LPAREN', 'RPAREN']:
        return ScopeSymbol.PAREN

class ScopeTree:
    def __init__(self,):
        self.__head = Scope(None, None)
        self.__pointer = self.__head

    def open_scope(self, symbol):
        new_scope = Scope(self.__pointer, get_scope_symbol_from_token(symbol.token_type))
        self.__pointer.children.append(new_scope)
        self.__pointer = new_scope

    def leave_scope(self, symbol, occurrence):
        if symbol.scope.symbol != self.__pointer.symbol:
            raise OutOfScopeException(symbol, f"Símbolo de {self.__pointer.symbol.value} não fechado")
        self.__pointer = self.__pointer.parent
        if self.__pointer is None:
            self.__pointer = self.__head
            raise OutOfScopeException(symbol, f"Contexto de um(a) "
                                              f"{get_scope_symbol_from_token(symbol.token_type).value} não aberto\n"
                                              f'linha: {occurrence.line} \n'
                                              f'coluna: {occurrence.column}')

    def check_end_of_input(self):
        if self.__head != self.__pointer:
            raise OutOfScopeException(self.__pointer.symbol, f"Símbolo de {self.__pointer.symbol.value} não fechado")

    @property
    def scope(self):
        return self.__pointer
