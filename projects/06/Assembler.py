from Parser import Parser
from SymbolsTable import SymbolsTable
from ToBinary import ToBinary
import sys


class Assembler:
    """
    this class represents the assembler
    """

    def __init__(self, filename):
        """
        the builder for the class
        :param filename: the file name that we want to read
        """

        self.__output = open(filename.split(".")[0] + ".hack", "w")
        parser = Parser(filename)
        parser.read_file()
        self.__lines = parser.get_lines()
        self.__symbols_table = SymbolsTable()

    def read_symbols(self):
        """
        this function extracts the symbols from the file
        :return: nothing
        """
        line_num = 0
        for line in self.__lines:  # reading labels
            if line.startswith('('):
                label = line[1:-1]
                self.__symbols_table.add_symbol(label, line_num)
            else:
                line_num += 1

        counter = 16
        for line in self.__lines:  # reading variables
            if "@" in line and ("0" > line[1] or line[1]) > "9":
                line = line.replace("@", "")
                variable = line
                if variable not in self.__symbols_table:
                    self.__symbols_table.add_symbol(variable, counter)
                    counter += 1

    def final_read(self):
        """
        this function that reads all the file again and replace all the symbols or numbers with their
         binary representation
        :return: nothing
        """
        for line in self.__lines:
            if "@" in line:
                if "0" <= line[1] <= "9":  # if it is a number
                    text = line[1:]
                else:  # if it is a symbol
                    text = self.__symbols_table.get_value(line[1:])
                text = bin(int(text))
                text = text[:1] + text[2:]
                if len(text) < 16:
                    text = ("0" * (16 - len(text))) + text
                self.__output.write(text + "\n")

            elif '=' in line or ';' in line:
                binary = "111"
                dest = ""
                comp = ""
                jump = ""
                if "=" in line and ";" in line:
                    lst1 = line.split("=")
                    lst2 = lst1[1].split(";")
                    dest = lst1[0]
                    comp = lst2[0]
                    jump = lst2[1]
                elif "=" in line:
                    lst = line.split("=")
                    dest = lst[0]
                    comp = lst[1]
                    jump = ""
                elif ";" in line:
                    lst = line.split(";")
                    dest = ""
                    comp = lst[0]
                    jump = lst[1]
                if "M" in comp:
                    binary += "1"
                else:
                    binary += "0"
                binary += ToBinary.comp(comp)
                binary += ToBinary.dest(dest)
                binary += ToBinary.jump(jump)
                self.__output.write(binary + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("invalid number of arguments")
    asm = Assembler(sys.argv[1])
    asm.read_symbols()
    asm.final_read()
