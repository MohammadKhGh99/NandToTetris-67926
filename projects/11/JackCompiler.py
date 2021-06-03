import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWriter import VMWriter
from SymbolTable import SymbolTable


class JackCompiler:

    def __init__(self, filename):
        if os.path.isdir(filename):
            flag = False
            for file in os.listdir(filename):
                if file.endswith(".jack"):
                    flag = True
                    input_file = open(filename + os.path.sep + os.path.basename(file), 'r')
                    tokenizer = JackTokenizer(input_file)
                    output_file = open(filename + os.path.sep + os.path.basename(file).replace(".jack", ".vm"), 'w')
                    vm_writer = VMWriter()
                    symbol_table = SymbolTable()
                    compiler = CompilationEngine(tokenizer, output_file, vm_writer, symbol_table)
                    output_file.write(compiler.compile_class())
                    output_file.close()
            if not flag:
                raise Exception("there is no jack files in the directory")
        elif os.path.exists(filename):
            input_file = open(filename, 'r')
            tokenizer = JackTokenizer(input_file)
            output_file = open(filename.replace(".jack", ".vm"), 'w')
            vm_writer = VMWriter()
            symbol_table = SymbolTable()
            compiler = CompilationEngine(tokenizer, output_file, vm_writer, symbol_table)
            output_file.write(compiler.compile_class())
            output_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("invalid number of inputs")
    jc = JackCompiler(sys.argv[1])
