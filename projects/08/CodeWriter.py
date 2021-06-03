from os import path


class CodeWriter:
    """
    class that convert each jack command to assembly
    """
    # counters to help naming the labels
    __counter = 0
    __call_counter = 0

    def __init__(self, filename):
        """
        the builder for the class
        :param filename: the file name
        """
        self.__filename = filename
        self.__segment_table = dict()
        self.__segment_table["local"] = "LCL"
        self.__segment_table["argument"] = "ARG"
        self.__segment_table["this"] = "THIS"
        self.__segment_table["that"] = "THAT"
        self.__segment_table["temp"] = "5"
        self.__segments = ["local", "argument", "this", "that", "temp", "constant", "static", "pointer"]
        self.__commands_table = dict()
        self.__commands_table["push"] = "@yyy\nD=M\n@xxx\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.__commands_table["pop"] = "@yyy\nD=M\n@xxx\nD=D+A\n@Point\nM=D\n@SP\nA=M-1\nD=M\n@Point\nA=M\nM=D\n" \
                                       "@SP\nM=M-1\n"
        self.__commands_table["add"] = "@SP\nA=M-1\nD=M\n@Some1\nM=D\n@2\nD=A\n@SP\nA=M-D\nD=M\n@Some1\nD=D+M\n" \
                                       "@RES\nM=D\n@SP\nM=M-1\n@RES\nD=M\n@SP\nA=M-1\nM=D\n"
        self.__commands_table["sub"] = "@SP\nA=M-1\nD=M\n@Some1\nM=D\n@2\nD=A\n@SP\nA=M-D\nD=M\n@Some1\nD=D-M\n" \
                                       "@RES\nM=D\n@SP\nM=M-1\n@RES\nD=M\n@SP\nA=M-1\nM=D\n"
        self.__commands_table["neg"] = "@SP\nA=M-1\nD=M\nD=-D\n@RES\nM=D\n@RES\nD=M\n@SP\nA=M-1\nM=D\n"
        self.__commands_table["eq_gt_lt"] = "@SP\nA=M-1\nD=M\n@Some1\nM=D\n@2\nD=A\n@SP\nA=M-D\nD=M\n@Some2\nM=D\n" \
                                            "@Some1\nD=M|D\n@CHECK_xxx\nD;JGE\n@Some1\nD=M\n@NEG_yyy\nD;JLE\n" \
                                            "@Some2\nD=M\n@CHECK_xxx\nD;JGE\n@Some1\nM=1\n@Some2\nM=0\n@CHECK_xxx\n" \
                                            "0;JMP\n(NEG_yyy)\n@Some2\nD=M\n@CHECK_xxx\nD;JLE\n@Some1\nM=0\n" \
                                            "@Some2\nM=1\n(CHECK_xxx)\n@Some2\nD=M\n@Some1\nD=D-M\n@RES\nM=-1\n" \
                                            "@END_IF_zzz\nD;jjj\n@RES\nM=0\n(END_IF_zzz)\n@SP\nM=M-1\n@RES\n" \
                                            "D=M\n@SP\nA=M-1\nM=D\n"
        self.__commands_table["and"] = "@SP\nA=M-1\nD=M\n@Some1\nM=D\n@2\nD=A\n@SP\nA=M-D\nD=M\n@Some1\nD=D&M\n" \
                                       "@RES\nM=D\n@SP\nM=M-1\n@RES\nD=M\n@SP\nA=M-1\nM=D\n"
        self.__commands_table["or"] = "@SP\nA=M-1\nD=M\n@Some1\nM=D\n@2\nD=A\n@SP\nA=M-D\nD=M\n@Some1\nD=D|M\n" \
                                      "@RES\nM=D\n@SP\nM=M-1\n@RES\nD=M\n@SP\nA=M-1\nM=D\n"
        self.__commands_table["not"] = "@SP\nA=M-1\nD=M\nD=!D\n@RES\nM=D\n@RES\nD=M\n@SP\nA=M-1\nM=D\n"
        self.__commands_table["pointer_push"] = "@xxx\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.__commands_table["pointer_pop"] = "@SP\nA=M-1\nD=M\n@xxx\nM=D\n@SP\nM=M-1\n"
        self.__commands_table["static_push"] = "@xxx\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.__commands_table["static_pop"] = "@xxx\nD=A\n@Point\nM=D\n@SP\nA=M-1\nD=M\n@Point\nA=M\nM=D\n@SP\nM=M-1\n"
        self.__commands_table["temp_push"] = "@xxx\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.__commands_table["temp_pop"] = "@xxx\nD=A\n@Point\nM=D\n@SP\nA=M-1\nD=M\n@Point\nA=M\nM=D\n@SP\nM=M-1\n"
        self.__commands_table["constant_push"] = "@xxx\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.__commands_table["label"] = "(xxx)\n"
        self.__commands_table["goto"] = "@xxx\n0;JMP\n"
        self.__commands_table["if-goto"] = "@SP\nAM=M-1\nD=M\n@xxx\nD;JNE\n"
        self.__commands_table["return"] = "@LCL\nD=M\n@FRAME\nM=D\n@5\nA=D-A\nD=M\n@RETURN\nM=D\n@SP\nA=M-1\nD=M\n" \
                                          "@ARG\nA=M\nM=D\n@SP\nM=M-1\n@ARG\nD=M\n@SP\nM=D+1\n@FRAME\nA=M-1\nD=M\n" \
                                          "@THAT\nM=D\n@FRAME\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n@FRAME\nD=M\n@3\n" \
                                          "A=D-A\nD=M\n@ARG\nM=D\n@FRAME\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n@RETURN\n" \
                                          "A=M\n0;JMP\n"
        self.__commands_table["call"] = "@GLOBAL_zzz\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n" \
                                        "@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\n" \
                                        "M=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@SP\nD=M\n@yyy\n" \
                                        "D=D-A\n@5\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@xxx\n0;JMP\n(GLOBAL_zzz)\n"
        self.__commands_table["args"] = "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
        self.__commands_table["init"] = "@256\nD=A\n@SP\nM=D\n"

    def write_init(self):
        """
        if we work with directory we need to do the bootstrap
        :return: command lines
        """
        assembly_commands = self.__commands_table["init"] + "\n"
        assembly_commands += self.read_call("call Sys.init 0")
        return assembly_commands

    def read_label(self, line):
        """
        reading label keyword
        :param line: the line to read
        :return: command lines
        """
        tokens = line.strip().split()
        assembly_commands = self.__commands_table[tokens[0]].replace("xxx", tokens[1])
        return assembly_commands

    def read_goto(self, line):
        """
        reading goto keyword
        :param line: the line to read
        :return: command lines
        """
        tokens = line.strip().split()
        if len(tokens) != 2:
            raise Exception("invalid goto command")
        assembly_commands = self.__commands_table[tokens[0]].replace("xxx", tokens[1])
        return assembly_commands

    def read_ifgoto(self, line):
        """
        reading if-goto keyword
        :param line: the line to read
        :return: command lines
        """
        tokens = line.strip().split()
        if len(tokens) != 2:
            raise Exception("invalid if-goto command")
        assembly_commands = self.__commands_table[tokens[0]].replace("xxx", tokens[1])
        return assembly_commands

    def read_function(self, line):
        """
        reading function keyword
        :param line: the line to read
        :return: command lines
        """
        tokens = line.strip().split()
        if len(tokens) != 3 or not tokens[2].isnumeric():
            raise Exception("invalid call command")
        assembly_commands = "({})\n".format(tokens[1])
        for i in range(int(tokens[2])):
            assembly_commands += self.__commands_table["args"]
        return assembly_commands

    def read_return(self, line):
        """
        reading return keyword
        :param line: the line to read
        :return: command lines
        """
        return self.__commands_table[line]

    def read_call(self, line):
        """
        reading call keyword
        :param line: the line to read
        :return: command lines
        """
        tokens = line.strip().split()
        if tokens[0] != "call":
            raise Exception("the first word should be call")
        if len(tokens) != 3 or not tokens[2].isnumeric():
            raise Exception("invalid call command")
        assembly_commands = self.__commands_table["call"]
        assembly_commands = assembly_commands.replace("xxx", tokens[1]).replace("yyy", tokens[2])
        assembly_commands = assembly_commands.replace("zzz", str(CodeWriter.__call_counter))
        CodeWriter.__call_counter += 1
        return assembly_commands

    def push_read(self, line, filename):
        """
        this method reads the push lines
        :param filename: the current file name
        :param line: the line to read
        :return: nothing
        """
        tokens = line.split()
        if len(tokens) != 3:
            raise Exception("invalid push line")
        push = tokens[0]
        if push != "push":
            raise Exception("the first word should be (push)")
        assembly_commands = self.__commands_table[push]
        segment = tokens[1]
        if segment not in self.__segments:  # checks the validity of the segment name
            raise Exception("invalid segment name")
        i = tokens[2]
        if not i.isnumeric():
            raise Exception("invalid segment index")
        if segment == "static":
            assembly_commands = self.__commands_table["static_push"]
            name = path.basename(filename)
            assembly_commands = assembly_commands.replace("xxx", name + i)
        elif segment == "pointer":
            assembly_commands = self.__commands_table["pointer_push"]
            if i != "0" and i != "1":
                raise Exception("pointer segment take just 1 or 0 index")
            if i == "1":
                assembly_commands = assembly_commands.replace("xxx", "THAT")
            else:
                assembly_commands = assembly_commands.replace("xxx", "THIS")
        elif segment == "constant":
            assembly_commands = self.__commands_table["constant_push"]
            assembly_commands = assembly_commands.replace("xxx", i)
        else:
            if segment == "temp":
                assembly_commands = self.__commands_table["temp_push"]
                assembly_commands = assembly_commands.replace("xxx", str(int(i) + 5))
            else:
                assembly_commands = assembly_commands.replace("xxx", i)
                assembly_commands = assembly_commands.replace("yyy", self.__segment_table[segment])
        return assembly_commands

    def pop_read(self, line, filename):
        """
        this method reads the pop lines
        :param filename: the current file name
        :param line: the line to read
        :return: nothing
        """
        tokens = line.split()
        if len(tokens) != 3:
            raise Exception("invalid push line")
        pop = tokens[0]
        if pop != "pop":
            raise Exception("the first word should be (pop)")
        assembly_commands = self.__commands_table[pop]
        segment = tokens[1]
        if segment == "constant":
            raise Exception("you can't pop to a constant")
        if segment not in self.__segments:
            raise Exception("invalid segment name")
        i = tokens[2]
        if not i.isnumeric():
            raise Exception("invalid segment index")
        if segment == "static":
            assembly_commands = self.__commands_table["static_pop"]
            name = path.basename(filename)
            assembly_commands = assembly_commands.replace("xxx", name + i)
        elif segment == "pointer":
            assembly_commands = self.__commands_table["pointer_pop"]
            if i != "1" and i != "0":
                raise Exception("pointer segment take just 1 or 0 index")
            if i == "1":
                assembly_commands = assembly_commands.replace("xxx", "THAT")
            else:
                assembly_commands = assembly_commands.replace("xxx", "THIS")
        elif segment == "temp":
            assembly_commands = self.__commands_table["temp_pop"]
            assembly_commands = assembly_commands.replace("xxx", str(int(i) + 5))
        else:
            assembly_commands = assembly_commands.replace("xxx", i)
            assembly_commands = assembly_commands.replace("yyy", self.__segment_table[segment])
        return assembly_commands

    def add_sub_neg_and_or_not_read(self, line):
        """
        this method reads the add lines
        :param line: the line to read
        :return: the command lines
        """
        return self.__commands_table[line]

    def eq_gt_lt_read(self, line):
        """
        this method to read eq, gt, lt keywords
        :param line: the line to read
        :return: command lines
        """
        assembly_commands = self.__commands_table["eq_gt_lt"]
        assembly_commands = assembly_commands.replace("xxx", str(CodeWriter.__counter))
        assembly_commands = assembly_commands.replace("yyy", str(CodeWriter.__counter))
        assembly_commands = assembly_commands.replace("zzz", str(CodeWriter.__counter))
        if line == "eq":
            assembly_commands = assembly_commands.replace("jjj", "JEQ")
        elif line == "gt":
            assembly_commands = assembly_commands.replace("jjj", "JGT")
        elif line == "lt":
            assembly_commands = assembly_commands.replace("jjj", "JLT")
        CodeWriter.__counter += 1
        return assembly_commands
