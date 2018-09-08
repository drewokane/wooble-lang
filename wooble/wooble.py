import sys

from functools import partial, reduce
from operator import mul, truediv, add, sub

from lark import Lark, Transformer, v_args
from lark.lexer import Token
from toolz.itertoolz import first, rest


@v_args(inline=True)
class WoobleTransformer(Transformer):
    number = float
    string = str

    def __init__(self, parser):
        self.execution_step = 0
        self.fns = {
            "def": self.define_variable,
            "*": partial(reduce, mul),
            "+": partial(reduce, add),
            "-": partial(reduce, sub),
            "/": partial(reduce, truediv)
            }
        self.user_fns = {}
        self.vars = {}
        self.parser = parser
    
    def parse_and_transform(self, expression):
        parsed = self.parser.parse(expression)
        transformed = self.transform(parsed)
        return transformed
    
    def function(self, fname, lp, params, rp, execution):
        self.user_fns[fname.value] = {
            "params": params.value.split(" "),
            "execution": execution.value
        }
        print(f"User functions: {self.user_fns}")
        #print(f"result: {self.parse_and_transform(execution.value)}")
        return [fname.value, params.value.split(" ")]

    def print_and_inc_ex_step(self, step, tokens):
        self.execution_step += 1
        print(f"Execution step: {self.execution_step} -> {step}")
        print(f"Tokens: {tokens}")

    def define_variable(self, args):
        self.print_and_inc_ex_step("define_variable", args)
        variable, value = args
        if not isinstance(variable, float):
            self.vars[variable] = value

    def variable(self, variable: Token):
        self.print_and_inc_ex_step("variable", variable)
        variable = variable.value
        return variable
    
    def contents(self, head, body):
        self.print_and_inc_ex_step("contents", [head, body])
        return [head, body]
    
    def head(self, head: Token):
        self.print_and_inc_ex_step("head", head)
        if head.value in self.fns.keys():
            fn = self.fns[head.value]
        else:
            def fn(*args):
                pass
        return fn
    
    def body(self, *body):
        self.print_and_inc_ex_step("body", body)
        return body
    
    def expression(self, lp, contents, rp):
        self.print_and_inc_ex_step("expression", contents)
        fn, args = contents
        args = [self.vars.get(a, a) for a in args]
        return fn(args)


def main(program):
    with open("wooble.lark", "r") as f:
        PARSER = Lark(f, start="program")
    
    TRANSFORMER = WoobleTransformer(PARSER)

    parsed = PARSER.parse(program)
    print(parsed.pretty())
    print("=" * 80)
    transformed = TRANSFORMER.transform(parsed)
    print(f"{TRANSFORMER.vars}")


if __name__ == '__main__':
    with open(sys.argv[1], "r") as program:
        main(program.read())