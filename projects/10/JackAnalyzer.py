import os
import sys

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackAnalyzer:

    def __init__(self, filename):
        if os.path.isdir(filename):
            flag = False
            for file in os.listdir(filename):
                if file.endswith(".jack"):
                    flag = True
                    if not os.path.exists(filename):
                        raise Exception("the file doesn't exist")
                    input_file = open(filename + os.path.sep + os.path.basename(file))
                    tokenizer = JackTokenizer(input_file)
                    output_file = open(filename + os.path.sep + os.path.basename(file).replace(".jack", ".xml"), 'w')
                    compiler = CompilationEngine(tokenizer, output_file)
                    output_file.write(compiler.compile_class())
                    output_file.close()
            if not flag:
                raise Exception("there is no jack files in the directory")
        else:
            if not os.path.exists(filename):
                raise Exception("the file doesn't exist")
            input_file = open(filename, 'r')
            tokenizer = JackTokenizer(input_file)
            output_file = open(filename.replace("jack", "xml"), 'w')
            compiler = CompilationEngine(tokenizer, output_file)
            output_file.write(compiler.compile_class())
            output_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("invalid number of inputs")
    jk = JackAnalyzer(sys.argv[1])
