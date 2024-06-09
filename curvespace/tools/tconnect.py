

from core.mincore import *


def tc(task):
    #T-shaped connect: 2 items, and their common abstractions
    answer = ai(task)
    answer = ai("what are common abstractions in this? which abstractions do you predict?", [task, answer])
    answer = ai(task, [answer])
    return answer

#tc("write me langauge for implicit interpretor that can handle non logical sentences")


class Interpreter:
    def __init__(self):
        self.variables = {}

    def tokenize(self, code):
        tokens = []
        for line in code.splitlines():
            tokens.append(line.split())
        return tokens

    def parse_expression(self, tokens):
        if tokens[0] == 'let':
            return self.parse_assignment(tokens[1:])
        elif tokens[0] == 'print':
            return self.parse_print(tokens[1:])
        else:
            raise SyntaxError("Invalid command")

    def parse_assignment(self, tokens):
        var_name = tokens[0]
        expr = tokens[1:]
        return {'type': 'assignment', 'var_name': var_name, 'expr': expr}

    def parse_print(self, tokens):
        expr = tokens[0]
        return {'type': 'print', 'expr': expr}

    def execute(self, expr):
        if expr['type'] == 'assignment':
            self.variables[expr['var_name']] = self.evaluate(expr['expr'])
        elif expr['type'] == 'print':
            print(self.evaluate(expr['expr']))

    def evaluate(self, expr):
        if expr[0].isdigit():
            return int(expr[0])
        elif expr[0] in self.variables:
            return self.variables[expr[0]]
        else:
            raise ValueError("Unknown variable")

    def run(self, code):
        tokensByLines = self.tokenize(code)
        for tokens in tokensByLines:
            if(len(tokens) == 0):
                continue
            expr = self.parse_expression(tokens)
            self.execute(expr)

# Example usage
interpreter = Interpreter()
code = """
let x 10
print x
let y 20
print y
"""
interpreter.run(code)

#x = "text1:ab", "text2:bxc"
#ai("connect 2 items in context", list(x))
