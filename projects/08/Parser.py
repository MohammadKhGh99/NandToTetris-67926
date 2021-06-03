import os


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
        if not os.path.isdir(self.__filename) and not os.path.exists(self.__filename):
            raise Exception("the file doesn't exist")
        all_files = list()
        lst = list()

        if os.path.isdir(self.__filename):
            files = os.listdir(self.__filename)
            for file in files:
                if file.endswith(".vm"):
                    all_files.append(file)
            if len(all_files) == 0:
                raise Exception("there is no .vm files in this directory")
            for file in all_files:
                base_path = os.getcwd()
                os.chdir(self.__filename)
                f = open(os.path.abspath(file), 'r')
                lst += f.readlines()
                os.chdir(base_path)
                f.close()
        else:
            file = open(self.__filename, 'r')
            lst = file.readlines()
            file.close()
        for line in lst:
            line = line.strip()
            if not line.startswith("//") and line != "\n" and line != "":
                if "/" in line:
                    i = line.index("/")
                    line = line[:i]
                self.__lines.append(line)

    def get_lines(self):
        return self.__lines
