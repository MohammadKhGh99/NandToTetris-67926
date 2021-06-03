from os import path


class Parser:
    """
    this class represents the parser for the files
    """

    def __init__(self, filename):
        """
        this builder for the class
        :param filename: the file name that we want to read
        """
        self.__filename = filename
        self.__lines = list()

    def read_file(self):
        """
        this function remove all useless sentences from the file
        :return: nothing
        """
        if not path.exists(self.__filename):
            raise Exception("the file doesn't exist")
        file = open(self.__filename, 'r')
        lst = file.readlines()

        for line in lst:
            line = line.replace(" ", "")
            line = line.replace("\n", "")
            if not line.startswith("//") and line != "":
                if "//" in line:
                    i = line.index("//")
                    line = line[:i]
                self.__lines.append(line)

    def get_lines(self):
        return self.__lines
