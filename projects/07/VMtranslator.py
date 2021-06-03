import sys
from Parser import Parser
from CodeWriter import CodeWriter
import os


class VMTranslator:
    """
    this class to convert a .vm file to .asm file
    """

    def __init__(self, filename):
        """
        the class's builder
        :param filename: the file name
        """
        if os.path.isdir(filename):
            self.__output = open(filename + os.path.sep + os.path.basename(filename) + ".asm", "w")
            self.__code = CodeWriter(filename)
        else:
            self.__output = open(filename[:-2] + "asm", 'w')
            name = os.path.basename(filename)
            self.__code = CodeWriter(name[:-2])
        parser = Parser(filename)
        parser.read_file()
        self.__lines = parser.get_lines()

    def final_read(self):
        """
        this method do the final read for the input file then write to the output file the appropriate lines
        :return: nothing
        """
        for line in self.__lines:
            if "push" in line:
                self.__output.write(self.__code.push_read(line) + "\n")
            elif "pop" in line:
                self.__output.write(self.__code.pop_read(line) + "\n")
            elif "add" in line:
                self.__output.write(self.__code.add_read(line) + "\n")
            elif "sub" in line:
                self.__output.write(self.__code.sub_read(line) + "\n")
            elif "neg" in line:
                self.__output.write(self.__code.neg_read(line) + "\n")
            elif "eq" in line:
                self.__output.write(self.__code.eq_read(line) + "\n")
            elif "gt" in line:
                self.__output.write(self.__code.gt_read(line) + "\n")
            elif "lt" in line:
                self.__output.write(self.__code.lt_read(line) + "\n")
            elif "and" in line:
                self.__output.write(self.__code.and_read(line) + "\n")
            elif "or" in line:
                self.__output.write(self.__code.or_read(line) + "\n")
            elif "not" in line:
                self.__output.write(self.__code.not_read(line) + "\n")
            else:
                raise Exception("invalid command line")
        self.__output.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("invalid number of arguments")
    vm_translator = VMTranslator(sys.argv[1])
    vm_translator.final_read()
