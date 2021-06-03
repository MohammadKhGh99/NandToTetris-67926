import JackTokenizer


class CompilationEngine:
    __statements = ["if", "else", "let", "while", "do", "return"]
    __op = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
    __unary_op = ['-', '~']
    __const_terms = ["true", "false", "this", "null"]
    __op_commands = {'-': "sub", '+': "add", '|': "or", "&amp;": "and", "&lt;": "lt", "&gt;": "gt", '=': "eq",
                     '*': "Math.multiply", '/': "Math.divide"}

    def __init__(self, tokenizer, output_file, vm_writer, symbol_table):
        self.__tokenizer = tokenizer
        self.__output = output_file
        self.__vm_writer = vm_writer
        self.__symbol_table = symbol_table
        self.__class_name = None
        self.__if_counter = self.__while_counter = 0
        self.__current_function = None

    def compile_class(self):
        """
        this method to read a whole class and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        i = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if i == 0:
                pass
            elif i == 1:
                self.__class_name = self.__tokenizer.get_token()
            elif i == 2:
                pass
            else:
                meth = self.__tokenizer.get_token() == "method"
                func = self.__tokenizer.get_token() == "function"
                constr = self.__tokenizer.get_token() == "constructor"
                if self.__tokenizer.get_token() == "static" or self.__tokenizer.get_token() == "field":
                    self.compile_class_var_dec()
                elif meth or func or constr:
                    self.__symbol_table.start_subroutine()
                    self.__if_counter = self.__while_counter = 0
                    commands += self.compile_subroutine_dec()
                else:
                    break
            i += 1
        return commands

    def compile_class_var_dec(self):
        """
        this method reads the class variables declarations and convert them to tokens
        :return: the tokens to write
        """
        cur_kind = self.__tokenizer.get_token()
        cur_type = ""
        i = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if i == 0:
                cur_type = self.__tokenizer.get_token()
            elif i == 1:
                name = self.__tokenizer.get_token()
                self.__symbol_table.define(name, cur_type, cur_kind)
            elif self.__tokenizer.get_token() == ';':
                break
            else:
                if self.__tokenizer.has_more_tokens():
                    self.__tokenizer.advance()
                    name = self.__tokenizer.get_token()
                    self.__symbol_table.define(name, cur_type, cur_kind)
            i += 1

    def compile_subroutine_dec(self):
        """
        this method reads a function, method, or a constructor and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        cur_type = self.__tokenizer.get_token()
        if cur_type == "method":
            self.__symbol_table.define("this", self.__class_name, "argument")
        i = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if i == 0:
                pass
            elif i == 1:
                self.__current_function = self.__class_name + '.' + self.__tokenizer.get_token()
            elif i == 2:
                pass
            elif i == 3:
                self.compile_parameter_list()
            elif i == 4:
                commands += self.compile_subroutine_body(cur_type)
                break
            else:
                break
            i += 1
        return commands

    def compile_parameter_list(self):
        """
        this method reads parameters list from a subroutine and convert it to tokens
        :return: the tokens to write
        """
        i = 0
        cur_type = None
        while self.__tokenizer.has_more_tokens():
            if self.__tokenizer.get_token() == ')':
                break
            elif self.__tokenizer.get_token() == ',':
                pass
            else:
                if i >= 0 and cur_type is None:
                    cur_type = self.__tokenizer.get_token()
                else:
                    self.__symbol_table.define(self.__tokenizer.get_token(), cur_type, "argument")
                    cur_type = None
            self.__tokenizer.advance()
            i += 1

    def compile_subroutine_body(self, cur_type):
        """
        this method reads a subroutine's body and converts it to tokens
        :return: the tokens to write
        """
        commands = ""
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if self.__tokenizer.get_token() != "var":
                break
            else:
                self.compile_var_dec()
        locals_num = self.__symbol_table.var_count("var")
        commands += self.__vm_writer.write_function(self.__current_function, locals_num)
        if cur_type == "constructor":
            n = self.__symbol_table.var_count("field")
            commands += self.__vm_writer.write_push("constant", n) + self.__vm_writer.write_call("Memory.alloc", 1)
            commands += self.__vm_writer.write_pop("pointer", 0)
        elif cur_type == "method":
            commands += self.__vm_writer.write_push("argument", 0) + self.__vm_writer.write_pop("pointer", 0)
        if self.__tokenizer.get_token() != '}':
            commands += self.compile_statements()
        return commands

    def compile_var_dec(self):
        """
        this method reads the variables declaration in subroutine and convert them to tokens
        :return: the tokens to write
        """
        cur_kind = self.__tokenizer.get_token()
        cur_type = ""
        i = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if i == 0:
                cur_type = self.__tokenizer.get_token()
            elif i == 1:
                self.__symbol_table.define(self.__tokenizer.get_token(), cur_type, cur_kind)
            else:
                if self.__tokenizer.get_token() != ';':
                    if self.__tokenizer.has_more_tokens():
                        self.__tokenizer.advance()
                        self.__symbol_table.define(self.__tokenizer.get_token(), cur_type, cur_kind)
                else:
                    break
            i += 1

    def statement_choices(self):
        """
        this function to help in making choice which statement is now? and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        if self.__tokenizer.get_token() == "return":
            commands += self.compile_return()
        elif self.__tokenizer.get_token() == "let":
            commands += self.compile_let()
        elif self.__tokenizer.get_token() == "do":
            commands += self.compile_do()
        elif self.__tokenizer.get_token() == "if":
            commands += self.compile_if()
        elif self.__tokenizer.get_token() == "while":
            commands += self.compile_while()
        return commands

    def compile_statements(self):
        """
        this method reads the statements in subroutine and convert them to tokens
        :return: the tokens to write
        """
        commands = self.statement_choices()
        while self.__tokenizer.get_token() in self.__statements:
            commands += self.statement_choices()
        return commands

    def compile_let(self):
        """
        this method reads a let statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        i = 0
        flag = False
        cur_kind = cur_index = ""
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if i == 0:
                cur_kind = self.__symbol_table.kind_of(self.__tokenizer.get_token())
                cur_index = self.__symbol_table.index_of(self.__tokenizer.get_token())
            elif i == 1:
                if self.__tokenizer.get_token() != '=':
                    flag = True
                    commands += self.__vm_writer.write_push(cur_kind, cur_index)
            elif i == 2 and flag:
                commands += self.compile_expression() + self.__vm_writer.write_arithmetic("add")
            elif i == 3 and flag:
                pass
            elif (i == 4 and flag) or (i == 2 and not flag):
                commands += self.compile_expression()
                if flag:
                    commands += self.__vm_writer.write_pop("temp", 0) + self.__vm_writer.write_pop("pointer", 1)
                    commands += self.__vm_writer.write_push("temp", 0) + self.__vm_writer.write_pop("that", 0)
                else:
                    commands += self.__vm_writer.write_pop(cur_kind, cur_index)
            else:
                break
            i += 1
        return commands

    def compile_if(self):
        """
        this method reads an if statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        i = 0
        if_counter = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if i == 0:
                pass
            elif i == 1:
                commands += self.compile_expression() + self.__vm_writer.write_arithmetic("not")
            elif i == 2:
                commands += self.__vm_writer.write_if("IF_FALSE_" + str(self.__if_counter))
                if_counter = self.__if_counter
                self.__if_counter += 1
            elif i == 3:
                commands += self.compile_statements()
            else:
                if self.__tokenizer.get_token() != "else":
                    commands += self.__vm_writer.write_label("IF_FALSE_" + str(if_counter))
                    break
                else:
                    commands += self.__vm_writer.write_goto("IF_TRUE_" + str(if_counter))
                    commands += self.__vm_writer.write_label("IF_FALSE_" + str(if_counter))
                    commands += self.compile_else() + self.__vm_writer.write_label("IF_TRUE_" + str(if_counter))
                    break
            i += 1
        return commands

    def compile_else(self):
        """
        this method reads an else statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        count = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if count == 0:
                pass
            elif count == 1:
                commands += self.compile_statements()
            else:
                break
            count += 1
        return commands

    def compile_while(self):
        """
        this method reads an while statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        commands += self.__vm_writer.write_label("WHILE_START_" + str(self.__while_counter))
        before = self.__while_counter
        self.__while_counter += 1
        i = 0
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if i == 0:
                pass
            elif i == 1:
                commands += self.compile_expression() + self.__vm_writer.write_arithmetic("not")
            elif i == 2:
                commands += self.__vm_writer.write_if("WHILE_END_" + str(before))
            elif i == 3:
                commands += self.compile_statements()
                commands += self.__vm_writer.write_goto("WHILE_START_" + str(before))
                commands += self.__vm_writer.write_label("WHILE_END_" + str(before))
            else:
                break
            i += 1
        return commands

    def compile_do(self):
        """
        this method reads a do statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        count = 0
        token = ""
        while self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if count == 0:
                token = self.__tokenizer.get_token()
            elif count == 1:
                commands += self.compile_subroutine_call(token, 0) + self.__vm_writer.write_pop("temp", 0)
            else:
                break
            count += 1
        return commands

    def compile_return(self):
        """
        this method reads a return statement in subroutine and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            if self.__tokenizer.get_token() == ';':
                commands += self.__vm_writer.write_push("constant", 0) + self.__vm_writer.write_return()
            else:
                commands += self.compile_expression() + self.__vm_writer.write_return()
        if self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
        return commands

    def compile_expression(self):
        """
        this method reads an expression and convert it to tokens
        :return: the tokens to write
        """
        commands = self.compile_term()
        while self.__tokenizer.has_more_tokens() and self.__tokenizer.get_token() in self.__op:
            cur_operator = self.__tokenizer.get_token()
            self.__tokenizer.advance()
            commands += self.compile_term()
            not_multiply = self.__op_commands[cur_operator] != "Math.multiply"
            not_divide = self.__op_commands[cur_operator] != "Math.divide"
            if not_multiply and not_divide:
                commands += self.__vm_writer.write_arithmetic(self.__op_commands[cur_operator])
            else:
                commands += self.__vm_writer.write_call(self.__op_commands[cur_operator], 2)
        return commands

    def __helper(self, letter):
        commands = self.__vm_writer.write_push("constant", ord(letter))
        commands += self.__vm_writer.write_call("String.appendChar", 2)
        return commands

    def compile_term(self):
        """
        this method reads a term and convert it to tokens
        :return: the tokens to write
        """
        commands = ""
        flag = None
        if self.__tokenizer.get_token() in self.__const_terms:
            if self.__tokenizer.get_token() == "true":
                commands += self.__vm_writer.write_push("constant", 0)
                commands += self.__vm_writer.write_arithmetic("not")
            elif self.__tokenizer.get_token() == "null" or self.__tokenizer.get_token() == "false":
                commands += self.__vm_writer.write_push("constant", 0)
            else:
                commands += self.__vm_writer.write_push("pointer", 0)
        elif self.__tokenizer.token_type() == JackTokenizer.STRING:
            commands += self.__vm_writer.write_push("constant", len(self.__tokenizer.get_token()))
            commands += self.__vm_writer.write_call("String.new", 1)
            commands += "".join(map(self.__helper, list(self.__tokenizer.get_token())))
        elif self.__tokenizer.token_type() == JackTokenizer.INT:
            commands += self.__vm_writer.write_push("constant", self.__tokenizer.get_token())
        elif self.__tokenizer.get_token() in self.__unary_op:
            cur_op = self.__tokenizer.get_token()
            if self.__tokenizer.has_more_tokens():
                self.__tokenizer.advance()
                commands += self.compile_term()
                if cur_op == '~':
                    commands += self.__vm_writer.write_arithmetic("not")
                else:
                    commands += self.__vm_writer.write_arithmetic("neg")
                flag = False
        elif self.__tokenizer.get_token() == '(' and self.__tokenizer.has_more_tokens():
            self.__tokenizer.advance()
            commands += self.compile_expression()
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
                    if before != "this":
                        cur_kind = self.__symbol_table.kind_of(before)
                        cur_index = self.__symbol_table.index_of(before)
                        commands += self.__vm_writer.write_push(cur_kind, cur_index)
                    else:
                        commands += self.__vm_writer.write_push("pointer", 0)
                        return commands
                elif after == '.' or after == '(':
                    commands += self.compile_subroutine_call(before, 0)
                elif after == '[':
                    cur_kind = self.__symbol_table.kind_of(before)
                    cur_index = self.__symbol_table.index_of(before)
                    commands += self.__vm_writer.write_push(cur_kind, cur_index)
                    if self.__tokenizer.has_more_tokens():
                        self.__tokenizer.advance()
                        commands += self.compile_expression() + self.__vm_writer.write_arithmetic("add")
                        commands += self.__vm_writer.write_pop("pointer", 1)
                        commands += self.__vm_writer.write_push("that", 0)
                        if self.__tokenizer.has_more_tokens():
                            self.__tokenizer.advance()
        return commands

    def compile_expression_list(self):
        """
        this method reads an expression list and convert it to tokens
        :return: the tokens to write
        """
        args = 0
        commands = ""
        while self.__tokenizer.has_more_tokens():
            if self.__tokenizer.get_token() != ',' and self.__tokenizer.get_token() != ')':
                commands += self.compile_expression()
                args += 1
            elif self.__tokenizer.get_token() == ',':
                if self.__tokenizer.has_more_tokens():
                    self.__tokenizer.advance()
            elif self.__tokenizer.get_token() == ')':
                return commands, args
        return commands, args

    def compile_subroutine_call(self, call, args):
        """
        this method reads a call statement and convert it to tokens
        :param args: args
        :param call: the caller
        :return: the tokens to write
        """
        commands = ""
        count = 0
        flag = False
        while self.__tokenizer.has_more_tokens():
            if self.__tokenizer.get_token() == '.' and count == 0:
                flag = True
            if flag is False and count > 0:
                self.__tokenizer.advance()
            if flag:
                self.__tokenizer.advance()
            if count == 0 and flag:
                if self.__tokenizer.get_token() == "this":
                    commands += self.__vm_writer.write_push("pointer", 0)
                    call = self.__class_name + '.' + call
                    args += 1
                else:
                    cur_type = self.__symbol_table.type_of(call)
                    cur_index = self.__symbol_table.index_of(call)
                    cur_kind = self.__symbol_table.kind_of(call)
                    if cur_kind is None or cur_index is None:
                        call += '.' + self.__tokenizer.get_token()
                    else:
                        commands += self.__vm_writer.write_push(cur_kind, cur_index)
                        call = cur_type + '.' + self.__tokenizer.get_token()
                        args += 1
            elif count == 1 and flag:
                pass
            elif count == 0 and flag is False:
                commands += self.__vm_writer.write_push("pointer", 0)
                call = self.__class_name + '.' + call
                args += 1
            elif (count == 1 and flag is False) or (count == 2 and flag):
                result = self.compile_expression_list()
                commands += result[0]
                args += result[1]
                commands += self.__vm_writer.write_call(call, args)
            elif (count == 2 and flag is False) or (count == 3 and flag):
                break
            else:
                break
            count += 1
        return commands
