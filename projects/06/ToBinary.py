class ToBinary:

    @staticmethod
    def comp(comp):
        """
        this function returns the binary representation of the given string
        :param comp: the string to convert
        :return: the binary representation of the given string
        """

        if comp == "0":
            return "101010"
        if comp == "1":
            return "111111"
        if comp == "-1":
            return "111010"
        if comp == "D":
            return "001100"
        if comp == "A" or comp == "M":
            return "110000"
        if comp == "!D":
            return "001101"
        if comp == "!A" or comp == "!M":
            return "110001"
        if comp == "-D":
            return "001111"
        if comp == "-A" or comp == "-M":
            return "110011"
        if comp == "D+1":
            return "011111"
        if comp == "A+1" or comp == "M+1":
            return "110111"
        if comp == "D-1":
            return "001110"
        if comp == "A-1" or comp == "M-1":
            return "110010"
        if comp == "D+A" or comp == "D+M":
            return "000010"
        if comp == "D-A" or comp == "D-M":
            return "010011"
        if comp == "A-D" or comp == "M-D":
            return "000111"
        if comp == "D&A" or comp == "D&M":
            return "000000"
        if comp == "D|A" or comp == "D|M":
            return "010101"

    @staticmethod
    def dest(dest):
        """
        this function returns the binary representation of the given string
        :param dest: the string to convert
        :return: the binary representation of the given string
        """

        if dest == "M":
            return "001"
        if dest == "D":
            return "010"
        if dest == "MD":
            return "011"
        if dest == "A":
            return "100"
        if dest == "AM":
            return "101"
        if dest == "AD":
            return "110"
        if dest == "AMD":
            return "111"
        return "000"

    @staticmethod
    def jump(jump):
        """
        this function returns the binary representation of the given string
        :param jump: the string to convert
        :return: the binary representation of the given string
        """
        if jump == "JGT":
            return "001"
        if jump == "JEQ":
            return "010"
        if jump == "JGE":
            return "011"
        if jump == "JLT":
            return "100"
        if jump == "JNE":
            return "101"
        if jump == "JLE":
            return "110"
        if jump == "JMP":
            return "111"
        return "000"
