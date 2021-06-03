import re

KEYWORD = "KEYWORD"
SYMBOL = "SYMBOL"
IDENTIFIER = "IDENTIFIER"
INT = "INT_CONST"
STRING = "STRING_CONST"


class JackTokenizer:

    def __init__(self, file):
        """
        builder which opens the .jack file and gets ready to tokenize it
        :param file: the file to tokenize
        """
        self.__current_token = None
        self.__current_type = None
        self.__lines = list()
        self.__counter = 0
        lst = file.readlines()
        for line in lst:
            line = line.strip()
            if_comment = (line.startswith("/**") or line.startswith("*") or line.startswith("*/"))
            if not line.startswith("//") and line != "\n" and line != "" and not if_comment:
                if "//" in line:
                    i = line.index("//")
                    line = line[:i]
                self.__lines.append(line)
        file.close()
        self.__current_line = self.__lines[0]
        self.__more_tokens = True
        self.__keywords_table = dict()
        self.__keywords_table["class"] = "<class>\n{}\n</class>\n"
        self.__keywords_table["method"] = "<method>\n{}\n</method>\n"
        self.__keywords_table["function"] = "<function>\n{}\n</function>\n"
        self.__keywords_table["constructor"] = "<constructor>\n{}\n</constructor>\n"
        self.__keywords_table["int"] = "<int>\n{}\n</int>\n"
        self.__keywords_table["boolean"] = "<boolean>\n{}\n</boolean>\n"
        self.__keywords_table["char"] = "<char>\n{}\n</char>\n"
        self.__keywords_table["void"] = "<void>\n{}\n</void>\n"
        self.__keywords_table["var"] = "<var>\n{}\n</var>\n"
        self.__keywords_table["static"] = "<static>\n{}\n</static>\n"
        self.__keywords_table["field"] = "<field>\n{}\n</field>\n"
        self.__keywords_table["let"] = "<let>\n{}\n</let>\n"
        self.__keywords_table["do"] = "<do>\n{}\n</do>\n"
        self.__keywords_table["if"] = "<if>\n{}\n</if>\n"
        self.__keywords_table["else"] = "<else>\n{}\n</else>\n"
        self.__keywords_table["while"] = "<while>\n{}\n</while>\n"
        self.__keywords_table["return"] = "<return>\n{}\n</return>\n"
        self.__keywords_table["true"] = "<true>\n{}\n</true>\n"
        self.__keywords_table["false"] = "<false>\n{}\n</false>\n"
        self.__keywords_table["null"] = "<null>\n{}\n</null>\n"
        self.__keywords_table["this"] = "<this>\n{}\n</this>\n"
        self.__symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.__tokens = list()
        self.__keywords = ["class", "method", "function", "constructor", "int", "boolean", "char", "void", "var",
                           "static", "field", "let", "do", "if", "else", "while", "return", "true", "false",
                           "null", "this"]

    def get_symbols(self):
        return self.__symbols

    def get_token(self):
        return self.__current_token

    def get_lines(self):
        return self.__lines

    def has_more_tokens(self):
        """
        method that checks if there are more tokens to read or not
        :return: True if there are more tokens to read, False otherwise
        """
        return self.__more_tokens

    def advance(self):
        """
        gets the next token from the input and makes it the current token
        :return:
        """
        if not self.__current_line:
            self.__current_token = self.__current_line
            return
        else:
            symbol = self.__current_line[0]
            if symbol == '"':
                self.__current_type = STRING
                string = self.__current_line[1:].split('"')
                self.__current_token = string[0]
                self.__current_line = string[1].strip()
            elif symbol in self.__symbols:
                self.__current_type = SYMBOL
                if len(self.__current_line) != 1:
                    self.__current_line = self.__current_line[1:]
                    self.__current_line = self.__current_line.strip()
                else:
                    self.__current_line = ""
                if symbol == '&':
                    self.__current_token = "&amp;"
                elif symbol == '<':
                    self.__current_token = "&lt;"
                elif symbol == '>':
                    self.__current_token = "&gt;"
                else:
                    self.__current_token = symbol
            else:
                matcher = re.compile("(\\w+)(.*)").match(self.__current_line)
                if matcher:
                    self.__current_token = matcher.group(1)
                    self.__current_line = matcher.group(2).strip()
                if self.__current_token.isnumeric():
                    self.__current_type = INT
                elif self.__current_token in self.__keywords:
                    self.__current_type = KEYWORD
                else:
                    self.__current_type = IDENTIFIER

            if self.__current_line == "":
                self.__counter += 1
                if self.__counter < len(self.__lines):
                    self.__current_line = self.__lines[self.__counter]
            return

    def token_type(self):
        """
        returns the type of the current token as a constant
        :return: the type of the current token as a constant
        """
        return self.__current_type
