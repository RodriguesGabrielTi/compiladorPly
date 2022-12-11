from enum import Enum


class ScopeSymbol(Enum):
    PAREN = "parenteses ')'"
    BRACE = "chaves '}'"
    BRACK = "colchete ']'"


class Scope:
    def __init__(self, parent, symbol: ScopeSymbol):
        self.__children: list[Scope] = []
        self.__parent: Scope = parent
        self.__symbol = symbol
        if self.__parent is None:
            self.__id: str = "0"
        else:
            self.__id: str = self.__parent.id + '/' + str(len(self.__parent.children))

    @property
    def id(self):
        return self.__id

    @property
    def children(self):
        return self.__children

    @property
    def parent(self):
        return self.__parent

    @property
    def symbol(self):
        return self.__symbol
