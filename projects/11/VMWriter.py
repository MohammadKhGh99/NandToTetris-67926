class VMWriter:
    __push_segments = ["constant", "argument", "local", "static", "temp", "pointer", "this", "that"]
    __pop_segments = ["argument", "local", "static", "temp", "pointer", "this", "that"]
    __ops = ["not", "neg", "or", "and", "lt", "gt", "eq", "sub", "add"]

    def __init__(self):
        pass

    def write_push(self, segment, index):
        if segment in self.__push_segments:
            return "push " + segment + ' ' + str(index) + '\n'
        else:
            raise Exception("invalid segment name")

    def write_pop(self, segment, index):
        if segment in self.__pop_segments:
            return "pop " + segment + ' ' + str(index) + '\n'
        elif segment == "constant":
            raise Exception("you can't pop to constant segment")
        else:
            raise Exception("invalid segment name")

    def write_arithmetic(self, command):
        if command in self.__ops:
            return command + '\n'
        else:
            raise Exception("invalid arithmetic command")

    def write_label(self, label):
        return "label " + label + '\n'

    def write_goto(self, label):
        return "goto " + label + '\n'

    def write_if(self, label):
        return "if-goto " + label + '\n'

    def write_call(self, name, num_args):
        return "call " + name + ' ' + str(num_args) + '\n'

    def write_function(self, name, num_locals):
        return "function " + name + ' ' + str(num_locals) + '\n'

    def write_return(self):
        return "return\n"
