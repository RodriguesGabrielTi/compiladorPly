from symbol_table.scope.scope_tree import ScopeTree
from symbol_table.symbol import Symbol, Occurrence
from tabulate import tabulate


class SymbolTable:
    def __init__(self):
        self.__program = None
        self.__symbols = []
        self.__scope_tree = ScopeTree()

    def add_symbol(self, new_symbol: Symbol, occurrence: Occurrence):
        new_symbol.scope = self.__scope_tree.scope
        if new_symbol.token_type in ['LBRACES', 'LPAREN', 'LBRACK']:
            self.__scope_tree.open_scope(new_symbol)
        if new_symbol.token_type in ['RBRACES', 'RPAREN', 'RBRACK']:
            self.__scope_tree.leave_scope(new_symbol, occurrence)
        if new_symbol.token_type == 'IDENT':
            for symbol in self.__symbols:
                if symbol.word == new_symbol.word and symbol.scope.id in new_symbol.scope.id:
                    symbol.occurrences.append(occurrence)
                    return
            new_symbol.occurrences.append(occurrence)
            self.__symbols.append(new_symbol)

    @property
    def symbols(self):
        return self.__symbols

    @property
    def program(self):
        return self.__program

    @program.setter
    def program(self, program):
        self.__program = program

    def pretty_print(self):
        table = []
        headers = ["Palavra", "Token", "Tipo", "Escopo", "Ocorrências"]
        table.append(headers)
        for symbol in self.__symbols:
            occurrences = ""
            for occurrence in symbol.occurrences:
                occurrences += "linha: " + str(occurrence.line) + " coluna: " + str(occurrence.column) + "\n"
            entry = [symbol.word, symbol.token_type, symbol.super_type.value, symbol.scope.id, occurrences]
            table.append(entry)
        print(tabulate(table, headers="firstrow"))

    def end(self):
        self.__scope_tree.check_end_of_input()

    def clear(self):
        self.__program = None
        self.__symbols = []
        self.__scope_tree = ScopeTree()
