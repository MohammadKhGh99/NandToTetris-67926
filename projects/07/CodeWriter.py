from os import path


class CodeWriter:
    """
    class that convert each jack command to assembly
    """
    # counter to help naming the labels
    __counter = 0

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
        # local, argument, this, that, temp
        self.__commands_table["push"] = "@xxx\nD=A\n@yyy\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        # local, argument, this, that, temp
        self.__commands_table["pop"] = "@xxx\nD=A\n@yyy\nD=M+D\n@R14\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R14\nA=M\nM=D\n"
        self.__commands_table["add"] = "@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=M+D\n"
        self.__commands_table["sub"] = "@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=M-D\n"
        self.__commands_table["neg"] = "@SP\nA=M-1\nM=!M\nM=M+1\n"
        self.__commands_table["eq"] = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\nM=0\n@JUMP_NUM\nD;JNE\n@SP\n" \
                                      "A=M\nM=-1\n(JUMP_NUM)\n@SP\nM=M+1\n"
        self.__commands_table["gt"] = "@32767\nD=!A\n@SP\nM=M-1\nA=M\nD=M&D\n@R14\nM=D\n@32767\nD=!A\n@SP\nA=M-1\n" \
                                      "D=M&D\n@R13\nM=D\n@R14\nD=D-M\n@Some_NUM\nD;JEQ\n@R13\nD=M\n@True_NUM\n" \
                                      "D;JEQ\n@SP\nA=M-1\nM=0\n@End_NUM\n0;JMP\n(Some_NUM)\n@SP\nA=M\nD=M\n@SP\n" \
                                      "M=M-1\nA=M\nD=M-D\nM=0\n@JUMP_NUM\nD;JLE\n@SP\nA=M\nM=-1\n(JUMP_NUM)\n@SP\n" \
                                      "M=M+1\n@End_NUM\n0;JMP\n(True_NUM)\n@SP\nA=M-1\nM=-1\n@End_NUM\n0;JMP\n" \
                                      "(End_NUM)\n"
        self.__commands_table["lt"] = "@32767\nD=!A\n@SP\nM=M-1\nA=M\nD=M&D\n@R14\nM=D\n@32767\nD=!A\n@SP\nA=M-1\n" \
                                      "D=M&D\n@R13\nM=D\n@R14\nD=D-M\n@Some_NUM\nD;JEQ\n@R14\nD=M\n@True_NUM\n" \
                                      "D;JEQ\n@SP\nA=M-1\nM=0\n@End_NUM\n0;JMP\n(Some_NUM)\n@SP\nA=M\nD=M\n" \
                                      "@SP\nM=M-1\nA=M\nD=M-D\nM=0\n@JUMP_NUM\nD;JGE\n@SP\nA=M\nM=-1\n(JUMP_NUM)\n" \
                                      "@SP\nM=M+1\n@End_NUM\n0;JMP\n(True_NUM)\n@SP\nA=M-1\nM=-1\n@End_NUM\n0;JMP\n" \
                                      "(End_NUM)\n"
        self.__commands_table["and"] = "@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=M&D\n"
        self.__commands_table["or"] = "@SP\nM=M-1\nA=M\nD=M\n@SP\nA=M-1\nM=M|D\n"
        self.__commands_table["not"] = "@SP\nA=M-1\nM=!M\n"
        self.__commands_table["static_pointer_push"] = "@xxx\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.__commands_table["static_pointer_pop"] = "@SP\nM=M-1\nA=M\nD=M\n@xxx\nM=D\n"
        self.__commands_table["temp_push"] = "@xxx\nD=A\n@yyy\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.__commands_table["temp_pop"] = "@xxx\nD=A\n@yyy\nD=A+D\n@R14\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R14\nA=M\nM=D\n"
        self.__commands_table["constant_push"] = "@xxx\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def push_read(self, line):
        """
        this method reads the push lines
        :param line: the line to read
        :return: nothing
        """
        push = line[:4]
        if push != "push":
            raise Exception("the first word should be (push)")
        assembly_commands = self.__commands_table[push]
        index = -1
        for j in range(len(line)):  # gets the index of the first number
            if "0" <= line[j] <= "9":
                index = j
                break
        if index == -1 or index == len(line):
            raise Exception("there is no index for the memory segment")
        segment = line[4:index]
        if segment not in self.__segments:  # checks the validity of the segment name
            raise Exception("invalid segment name")
        i = line[index:]
        if not i.isnumeric():
            raise Exception("invalid segment index")

        if segment == "static" or segment == "pointer":
            assembly_commands = self.__commands_table["static_pointer_push"]
            name = path.basename(self.__filename)
            if segment == "static":
                assembly_commands = assembly_commands.replace("xxx", name + i)
            else:  # pointer
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
            assembly_commands = assembly_commands.replace("xxx", i)
            assembly_commands = assembly_commands.replace("yyy", self.__segment_table[segment])
        return assembly_commands

    def pop_read(self, line):
        """
        this method reads the pop lines
        :param line: the line to read
        :return: nothing
        """
        pop = line[:3]
        if pop != "pop":
            raise Exception("the first word should be (pop)")
        assembly_commands = self.__commands_table[pop]
        index = -1
        for j in range(len(line)):
            if "0" <= line[j] <= "9":
                index = j
                break
        if index == -1 or index == len(line):
            raise Exception("there is no index for the segment")
        segment = line[3:index]
        if segment == "constant":
            raise Exception("you can't pop to a constant")
        if segment not in self.__segments:
            raise Exception("invalid segment name")
        i = line[index:]
        if not i.isnumeric():
            raise Exception("invalid segment index")

        if segment == "static" or segment == "pointer":
            assembly_commands = self.__commands_table["static_pointer_pop"]
            name = path.basename(self.__filename)
            if segment == "static":
                assembly_commands = assembly_commands.replace("xxx", name + i)
            else:
                if i != "1" and i != "0":
                    raise Exception("pointer segment take just 1 or 0 index")
                if i == "1":
                    assembly_commands = assembly_commands.replace("xxx", "THAT")
                else:
                    assembly_commands = assembly_commands.replace("xxx", "THIS")
        else:
            if segment == "temp":
                assembly_commands = self.__commands_table["temp_pop"]
            assembly_commands = assembly_commands.replace("xxx", i)
            assembly_commands = assembly_commands.replace("yyy", self.__segment_table[segment])
        return assembly_commands

    # we could merge the three methods, add_read, sub_read, and_read, not_read, neg_read to one method
    def add_read(self, line):
        """
        this method reads the add lines
        :param line: the line to read
        :return: nothing
        """
        add = line[:3]
        if add != "add":
            raise Exception("the first word should be (add)")
        if len(line) != len(add):
            raise Exception("the line should contain only (add) word")
        return self.__commands_table[add]

    # we could merge the three methods, add_read, sub_read, and_read, not_read, neg_read to one method
    def sub_read(self, line):
        """
        this method reads the sub lines
        :param line: the line to read
        :return: nothing
        """
        sub = line[:3]
        if sub != "sub":
            raise Exception("the first word should be (sub)")
        if len(line) != len(sub):
            raise Exception("the line should contain only (sub) word")
        return self.__commands_table[sub]

    # we could merge the three methods, add_read, sub_read, and_read, not_read, neg_read to one method
    def neg_read(self, line):
        """
        this method reads the neg lines
        :param line: the line to read
        :return: nothing
        """
        neg = line[:3]
        if neg != "neg":
            raise Exception("the first word should be (neg)")
        if len(line) != len(neg):
            raise Exception("the line should contain only (neg) word")
        return self.__commands_table[neg]

    # we could merge the three methods, eq_read, gt_read, lt_read to one method
    def eq_read(self, line):
        """
        this method reads the eq lines
        :param line: the line to read
        :return: nothing
        """
        eq = line[:2]
        if eq != "eq":
            raise Exception("the first word should be (eq)")
        if len(line) != len(eq):
            raise Exception("the line should contain only (eq) word")
        assembly_commands = self.__commands_table[eq]
        assembly_commands = assembly_commands.replace("NUM", str(CodeWriter.__counter))
        CodeWriter.__counter += 1
        return assembly_commands

    # we could merge the three methods, eq_read, gt_read, lt_read to one method
    def gt_read(self, line):
        """
        this method reads the gt lines
        :param line: the line to read
        :return: nothing
        """
        gt = line[:2]
        if gt != "gt":
            raise Exception("the first word should be (gt)")
        if len(line) != len(gt):
            raise Exception("the line should contain only (gt) word")
        assembly_commands = self.__commands_table[gt]
        assembly_commands = assembly_commands.replace("NUM", str(CodeWriter.__counter))
        CodeWriter.__counter += 1
        return assembly_commands

    # we could merge the three methods, eq_read, gt_read, lt_read to one method
    def lt_read(self, line):
        """
        this method reads the lt lines
        :param line: the line to read
        :return: nothing
        """
        lt = line[:2]
        if lt != "lt":
            raise Exception("the first word should be (lt)")
        if len(line) != len(lt):
            raise Exception("the line should contain only (lt) word")
        assembly_commands = self.__commands_table[lt]
        assembly_commands = assembly_commands.replace("NUM", str(CodeWriter.__counter))
        CodeWriter.__counter += 1
        return assembly_commands

    # we could merge the three methods, add_read, sub_read, and_read, not_read, neg_read to one method
    def and_read(self, line):
        """
        this method reads the and lines
        :param line: the line to read
        :return: nothing
        """
        _and = line[:3]
        if _and != "and":
            raise Exception("the first word should be (and)")
        if len(line) != len(_and):
            raise Exception("the line should contain only (and) word")
        return self.__commands_table[_and]

    def or_read(self, line):
        """
        this method reads the or lines
        :param line: the line to read
        :return: nothing
        """
        _or = line[:2]
        if _or != "or":
            raise Exception("the first word should be (or)")
        if len(line) != len(_or):
            raise Exception("the line should contain only (or) word")
        return self.__commands_table[_or]

    # we could merge the three methods, add_read, sub_read, and_read, not_read, neg_read to one method
    def not_read(self, line):
        """
        this method reads the not lines
        :param line: the line to read
        :return: nothing
        """
        _not = line[:3]
        if _not != "not":
            raise Exception("the first word should be (not)")
        if len(line) != len(_not):
            raise Exception("the line should contain only (not) word")
        return self.__commands_table[_not]
