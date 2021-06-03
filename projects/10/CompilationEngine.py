import JackTokenizer


class CompilationEngine:

    def __init__(self, tokenizer, output_file):
        self.__tokenizer = tokenizer
        self.__tokens = ""
        self.__tabs = 0
        self.__output_file = output_file
        self.__table = dict()
        self.__class = "<class>\n{}</class>\n"
        self.__class_var_dec = "<classVarDec>\n{}</classVarDec>\n"
        self.__subroutine_dec = "<subroutineDec>\n{}</subroutineDec>\n"
        self.__subroutine_body = "<subroutineBody>\n{}</subroutineBody>\n"
        self.__parameter_list = "<parameterList>\n{}</parameterList>\n"
        self.__statements_tags = "<statements>\n{}</statements>\n"
        self.__return_statement = "<returnStatement>\n{}</returnStatement>\n"
        self.__expression = "<expression>\n{}</expression>\n"
        self.__term = "<term>\n{}</term>\n"
        self.__keyword = "<keyword> {} </keyword>\n"
        self.__identifier = "<identifier> {} </identifier>\n"
        self.__symbol = "<symbol> {} </symbol>\n"
        self.__let_statement = "<letStatement>\n{}</letStatement>\n"
        self.__expression_list = "<expressionList>\n{}</expressionList>\n"
        self.__do_statement = "<doStatement>\n{}</doStatement>\n"
        self.__if_statement = "<ifStatement>\n{}</ifStatement>\n"
        self.__while_statement = "<whileStatement>\n{}</whileStatement>\n"
        self.__integer_constant = "<integerConstant> {} </integerConstant>\n"
        self.__string_constant = "<stringConstant> {} </stringConstant>\n"
        self.__var_dec = "<varDec>\n{}</varDec>\n"
        self.__types = ["int", "char", "boolean"]
        self.__className = ""
        self.__op = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
        self.__unary_op = ['-', '~']
        self.__const_terms = ["true", "false", "this", "null"]
        self.__statements = ["if", "else", "let", "while", "do", "return"]

    def compile_class(self):
        """
        this method to read a whole class and convert it to tokens
        :return: the tokens to write
        """
        content = ""
        counter = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if counter == 0:
                content += self.__keyword.format(self.__tokenizer.get_token())
            elif counter == 1:
                content += self.__identifier.format(self.__tokenizer.get_token())
            elif counter == 2:
                content += self.__symbol.format(self.__tokenizer.get_token())
            else:
                meth = self.__tokenizer.get_token() == "method"
                func = self.__tokenizer.get_token() == "function"
                constr = self.__tokenizer.get_token() == "constructor"
                if meth or func or constr:
                    content += self.compile_subroutine_dec()
                elif self.__tokenizer.get_token() == "static" or self.__tokenizer.get_token() == "field":
                    content += self.compile_class_var_dec()
                else:
                    content += self.__symbol.format(self.__tokenizer.get_token())
                    break
            counter += 1
        return self.__class.format(content)

    def compile_class_var_dec(self):
        """
        this method reads the class variables declarations and convert them to tokens
        :return: the tokens to write
        """
        content = self.__keyword.format(self.__tokenizer.get_token())
        counter = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if counter == 0:
                if self.__tokenizer.token_type() != JackTokenizer.KEYWORD:
                    content += self.__identifier.format(self.__tokenizer.get_token())
                else:
                    content += self.__keyword.format(self.__tokenizer.get_token())
            elif counter == 1:
                content += self.__identifier.format(self.__tokenizer.get_token())
            elif self.__tokenizer.get_token() == ';':
                content += self.__symbol.format(';')
                break
            else:
                content += self.__symbol.format(self.__tokenizer.get_token())
                if self.__tokenizer.has_more_tokens():
                    self.__tokenizer.advance()
                    content += self.__identifier.format(self.__tokenizer.get_token())
            counter += 1
        return self.__class_var_dec.format(content)

    def compile_subroutine_dec(self):
        """
        this method reads a function, method, or a constructor and convert it to tokens
        :return: the tokens to write
        """
        content = self.__keyword.format(self.__tokenizer.get_token())
        counter = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if counter == 0:
                if self.__tokenizer.token_type() != JackTokenizer.KEYWORD:
                    content += self.__identifier.format(self.__tokenizer.get_token())
                else:
                    content += self.__keyword.format(self.__tokenizer.get_token())
            elif counter == 1:
                content += self.__identifier.format(self.__tokenizer.get_token())
            elif counter == 2:
                content += self.__symbol.format(self.__tokenizer.get_token())
            elif counter == 3:
                content += self.compile_parameter_list()
                content += self.__symbol.format(self.__tokenizer.get_token())
            elif counter == 4:
                content += self.compile_subroutine_body()
                break
            else:
                break
            counter += 1
        return self.__subroutine_dec.format(content)

    def compile_parameter_list(self):
        """
        this method reads parameters list from a subroutine and convert it to tokens
        :return: the tokens to write
        """
        content = ""
        while self.__tokenizer.has_more_tokens():
            if self.__tokenizer.get_token() == ')':
                break
            if self.__tokenizer.token_type() == JackTokenizer.KEYWORD:
                content += self.__keyword.format(self.__tokenizer.get_token())
            elif self.__tokenizer.get_token() == ',':
                content += self.__symbol.format(self.__tokenizer.get_token())
            else:
                content += self.__identifier.format(self.__tokenizer.get_token())
            self.__tokenizer.advance()
        return self.__parameter_list.format(content)

    def compile_subroutine_body(self):
        """
        this method reads a subroutine's body and converts it to tokens
        :return: the tokens to write
        """
        content = self.__symbol.format('{')
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if self.__tokenizer.get_token() != "var":
                break
            else:
                content += self.compile_var_dec()
        if self.__tokenizer.get_token() != '}':
            content += self.compile_statements()
        content += self.__symbol.format('}')
        return self.__subroutine_body.format(content)

    def compile_var_dec(self):
        """
        this method reads the variables declaration in subroutine and convert them to tokens
        :return: the tokens to write
        """
        content = self.__keyword.format(self.__tokenizer.get_token())
        counter = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if counter == 0:
                if self.__tokenizer.token_type() != JackTokenizer.KEYWORD:
                    content += self.__identifier.format(self.__tokenizer.get_token())
                else:
                    content += self.__keyword.format(self.__tokenizer.get_token())
            elif counter == 1:
                content += self.__identifier.format(self.__tokenizer.get_token())
            else:
                if self.__tokenizer.get_token() != ';':
                    content += self.__symbol.format(self.__tokenizer.get_token())
                    if self.__tokenizer.has_more_tokens():
                        self.__tokenizer.advance()
                        content += self.__identifier.format(self.__tokenizer.get_token())
                else:
                    content += self.__symbol.format(self.__tokenizer.get_token())
                    break
            counter += 1
        return self.__var_dec.format(content)

    def statement_choices(self):
        """
        this function to help in making choice which statement is now? and convert it to tokens
        :return: the tokens to write
        """
        content = ""
        if self.__tokenizer.get_token() == "return":
            content += self.compile_return()
        elif self.__tokenizer.get_token() == "let":
            content += self.compile_let()
        elif self.__tokenizer.get_token() == "do":
            content += self.compile_do()
        elif self.__tokenizer.get_token() == "if":
            content += self.compile_if()
        elif self.__tokenizer.get_token() == "while":
            content += self.compile_while()
        return content

    def compile_statements(self):
        """
        this method reads the statements in subroutine and convert them to tokens
        :return: the tokens to write
        """
        content = self.statement_choices()
        while self.__tokenizer.get_token() in self.__statements:
            content += self.statement_choices()
        return self.__statements_tags.format(content)

    def compile_let(self):
        """
        this method reads a let statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        content = self.__keyword.format(self.__tokenizer.get_token())
        count = 0
        flag = False
        counter = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if flag:
                if counter == 0:
                    content += self.compile_expression() + self.__symbol.format(self.__tokenizer.get_token())
                elif counter == 1:
                    flag = False
                    count += 1
                    content += self.__symbol.format(self.__tokenizer.get_token())

                counter += 1
                continue
            if count == 0:
                content += self.__identifier.format(self.__tokenizer.get_token())
            elif count == 1:
                content += self.__symbol.format(self.__tokenizer.get_token())
                if self.__tokenizer.get_token() != '=':
                    if self.__tokenizer.has_more_tokens():
                        flag = True
                        continue
            elif count == 2:
                content += self.compile_expression() + self.__symbol.format(self.__tokenizer.get_token())
            else:
                break
            count += 1
        return self.__let_statement.format(content)

    def if_while(self, if_if):
        """
        this function to help in reading if and while statements
        :param if_if: if the function has been called from if statement
        :return: the token to read
        """
        content = self.__keyword.format(self.__tokenizer.get_token())
        count = 0
        while self.__tokenizer.has_more_tokens():
            if if_if == 1 and self.__tokenizer.get_token() == '}':
                break
            self.__tokenizer.advance()
            if count == 0:
                content += self.__symbol.format(self.__tokenizer.get_token())
            elif count == 1:
                content += self.compile_expression() + self.__symbol.format(self.__tokenizer.get_token())
            elif count == 2:
                content += self.__symbol.format(self.__tokenizer.get_token())
            elif count == 3:
                content += self.compile_statements() + self.__symbol.format(self.__tokenizer.get_token())
            else:
                break
            count += 1
        return content

    def compile_if(self):
        """
        this method reads an if statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        content = self.if_while(1)
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if self.__tokenizer.get_token() == "else":
                content += self.compile_else()
        return self.__if_statement.format(content)

    def compile_else(self):
        """
        this method reads an else statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        content = self.__keyword.format("else")
        count = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if count == 0:
                content += self.__symbol.format(self.__tokenizer.get_token())
            elif count == 1:
                content += self.compile_statements() + self.__symbol.format(self.__tokenizer.get_token())
            else:
                break
            count += 1
        return content

    def compile_while(self):
        """
        this method reads an while statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        return self.__while_statement.format(self.if_while(0))

    def compile_do(self):
        """
        this method reads a do statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        content = self.__keyword.format(self.__tokenizer.get_token())
        count = 0
        token = ""
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if count == 0:
                token = self.__tokenizer.get_token()
            elif count == 1:
                content += self.compile_subroutine_call(token) + self.__symbol.format(self.__tokenizer.get_token())
            else:
                break
            count += 1
        return self.__do_statement.format(content)

    def compile_return(self):
        """
        this method reads a return statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        content = self.__keyword.format(self.__tokenizer.get_token())
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if self.__tokenizer.get_token() != ';':
                content += self.compile_expression()
            content += self.__symbol.format(self.__tokenizer.get_token())
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
        return self.__return_statement.format(content)

    def compile_expression(self):
        """
        this method reads an expression and convert it to tokens
        :return: the tokens to write
        """
        content = self.compile_term()
        while self.__tokenizer.has_more_tokens() and self.__tokenizer.get_token() in self.__op:
            content += self.__symbol.format(self.__tokenizer.get_token())
            self.__tokenizer.advance()
            content += self.compile_term()
        return self.__expression.format(content)

    def compile_term(self):
        """
        this method reads a term and convert it to tokens
        :return: the tokens to write
        """
        content = ""
        flag = None
        if self.__tokenizer.get_token() in self.__const_terms:
            content += self.__keyword.format(self.__tokenizer.get_token())
        elif self.__tokenizer.token_type() == JackTokenizer.STRING:
            content += self.__string_constant.format(self.__tokenizer.get_token())
        elif self.__tokenizer.token_type() == JackTokenizer.INT:
            content += self.__integer_constant.format(self.__tokenizer.get_token())
        elif self.__tokenizer.get_token() in self.__unary_op:
            content += self.__symbol.format(self.__tokenizer.get_token())
            if self.__tokenizer.has_more_tokens():
                self.__tokenizer.advance()
                content += self.compile_term()
                flag = False
        elif self.__tokenizer.get_token() == '(':
            content += self.__symbol.format(self.__tokenizer.get_token())
            if self.__tokenizer.has_more_tokens():
                self.__tokenizer.advance()
                content += self.compile_expression() + self.__symbol.format(self.__tokenizer.get_token())
        else:
            flag = True
        if flag is None and self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            flag = False
        if flag:
            before = self.__tokenizer.get_token()
            if self.__tokenizer.has_more_tokens():
                self.__tokenizer.advance()
                after = self.__tokenizer.get_token()
                if after != '[' and after != '.' and after != '(':
                    content += self.__identifier.format(before)
                elif after == '.' or after == '(':
                    content += self.compile_subroutine_call(before)
                elif after == '[':
                    content += self.__identifier.format(before) + self.__symbol.format('[')
                    if self.__tokenizer.has_more_tokens():
                        self.__tokenizer.advance()
                        content += self.compile_expression() + self.__symbol.format(self.__tokenizer.get_token())
                        if self.__tokenizer.has_more_tokens():
                            self.__tokenizer.advance()
        return self.__term.format(content)

    def compile_expression_list(self):
        """
        this method reads an expression list and convert it to tokens
        :return: the tokens to write
        """
        content = ""
        counter = 0
        while self.__tokenizer.has_more_tokens():
            if self.__tokenizer.get_token() == ',':
                content += self.__symbol.format(self.__tokenizer.get_token())
                if self.__tokenizer.has_more_tokens():
                    self.__tokenizer.advance()
            elif self.__tokenizer.get_token() == ')':
                break
            else:
                content += self.compile_expression()
            counter += 1
        return self.__expression_list.format(content)

    def compile_subroutine_call(self, call):
        """
        this method reads a call statement and convert it to tokens
        :param call: the caller
        :return: the tokens to write
        """
        content = self.__identifier.format(call) + self.__symbol.format(self.__tokenizer.get_token())
        count = 0
        flag = False
        while self.__tokenizer.has_more_tokens():
            if self.__tokenizer.get_token() == '.' and count == 0:
                flag = True
            self.__tokenizer.advance()
            if count == 0 and flag:
                content += self.__identifier.format(self.__tokenizer.get_token())
            elif count == 1 and flag:
                content += self.__symbol.format(self.__tokenizer.get_token())
            elif count == 0 or (count == 2 and flag):
                content += self.compile_expression_list() + self.__symbol.format(self.__tokenizer.get_token())
            else:
                break
            count += 1
        return content

    def get_tokens(self):
        return self.__tokens
