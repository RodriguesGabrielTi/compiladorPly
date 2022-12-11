class OutOfScopeException(Exception):
    def __init__(self, symbol, message):
        self.__symbol = symbol
        super().__init__(message)

    @property
    def symbol(self):
        return self.__symbol

