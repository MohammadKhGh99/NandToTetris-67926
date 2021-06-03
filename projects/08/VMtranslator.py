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
        self.__filename = filename
        self.__lines = parser.get_lines()

    def final_read(self):
        """
        this method do the final read for the input file then write to the output file the appropriate lines
        :return: nothing
        """
        current_filename = self.__filename
        if os.path.isdir(self.__filename):
            self.__output.write(self.__code.write_init() + "\n")
        for line in self.__lines:
            line = line.strip()
            # self.__output.write("// " + line + "\n")
            if line.startswith("push"):
                self.__output.write(self.__code.push_read(line, current_filename) + "\n")
            elif line.startswith("pop"):
                self.__output.write(self.__code.pop_read(line, current_filename) + "\n")
            elif "add" == line or "sub" == line or "neg" == line or "and" == line or "or" == line or "not" == line:
                self.__output.write(self.__code.add_sub_neg_and_or_not_read(line) + "\n")
            elif "eq" == line or "gt" == line or "lt" == line:
                self.__output.write(self.__code.eq_gt_lt_read(line) + "\n")
            elif line.startswith("function"):
                func = line.split()[1]
                current_filename = func[:func.index('.')]
                self.__output.write(self.__code.read_function(line) + "\n")
            elif line.startswith("call"):
                self.__output.write(self.__code.read_call(line) + "\n")
            elif line.startswith("if-goto"):
                self.__output.write(self.__code.read_ifgoto(line) + "\n")
            elif line.startswith("goto"):
                self.__output.write(self.__code.read_goto(line) + "\n")
            elif line.startswith("label"):
                self.__output.write(self.__code.read_label(line) + "\n")
            elif "return" == line:
                self.__output.write(self.__code.read_return(line) + "\n")
            else:
                raise Exception("invalid command line")
        self.__output.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("invalid number of arguments")
    vm_translator = VMTranslator(sys.argv[1])
    vm_translator.final_read()
