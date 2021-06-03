class SymbolTable:

    def __init__(self):
        self.__class_symbols = dict()
        self.__subroutine_symbols = dict()
        self.__running_index = {"field": 0, "static": 0, "argument": 0, "var": 0}  # var = local

    def get_class_symbols(self):
        return self.__class_symbols

    def get_subroutine_symbols(self):
        return self.__subroutine_symbols

    def start_subroutine(self):
        self.__subroutine_symbols.clear()
        self.__running_index["var"] = self.__running_index["argument"] = 0

    def define(self, name, i_type, kind):
        if kind == "field" or kind == "static" or kind == "argument" or kind == "var":
            cur_index = self.__running_index[kind]
            if kind == "field" or kind == "static":
                self.__class_symbols[name] = (i_type, kind, cur_index)
            elif kind == "argument" or kind == "var":
                self.__subroutine_symbols[name] = (i_type, kind, cur_index)
            self.__running_index[kind] += 1

    def var_count(self, kind):
        return self.__running_index[kind] if kind in self.__running_index else 0

    def kind_of(self, name):
        if name in self.__class_symbols:
            return self.__class_symbols[name][1] if self.__class_symbols[name][1] != "field" else "this"
        elif name in self.__subroutine_symbols:
            return self.__subroutine_symbols[name][1] if self.__subroutine_symbols[name][1] != "var" else "local"
        else:
            return None

    def type_of(self, name):
        if name in self.__class_symbols:
            return self.__class_symbols[name][0]
        elif name in self.__subroutine_symbols:
            return self.__subroutine_symbols[name][0]
        else:
            return None

    def index_of(self, name):
        if name in self.__class_symbols:
            return self.__class_symbols[name][2]
        elif name in self.__subroutine_symbols:
            return self.__subroutine_symbols[name][2]
        else:
            return None
