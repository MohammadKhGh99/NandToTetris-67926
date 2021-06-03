class SymbolsTable:
    """
    this class represents the symbols table
    """

    def __init__(self):
        """
        this builder for the class
        """

        self.__symbols = dict()
        for i in range(16):
            self.__symbols["R" + str(i)] = i
        self.__symbols["SCREEN"] = 16384
        self.__symbols["KBD"] = 24576
        self.__symbols["SP"] = 0
        self.__symbols["LCL"] = 1
        self.__symbols["ARG"] = 2
        self.__symbols["THIS"] = 3
        self.__symbols["THAT"] = 4

    def add_symbol(self, symbol, value):
        """
        this function to add a symbol to the symbols table
        :param symbol: the symbol to add
        :param value: the value of the given symbol
        """
        self.__symbols[symbol] = value

    def __contains__(self, symbol):
        """
        this function to add the functionality to the class to use "in" word to check if the given
        item is in the table or not
        :param symbol: the symbol to search for
        :return: 1 if it is in the table, 0 otherwise
        """
        return 1 if symbol in self.__symbols.keys() else 0

    def get_value(self, symbol):
        """
        this function to get the given symbol's value from the table
        :param symbol: the symbol to get its value
        :return: the symbol's value
        """
        return self.__symbols[symbol]

    def get_symbols(self):
        return self.__symbols
