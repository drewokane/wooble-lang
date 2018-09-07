from functools import partial, reduce
from operator import mul, truediv, add, sub

from lark import Lark, Transformer, v_args
from lark.lexer import Token
from toolz.itertoolz import first, rest


@v_args(inline=True)
class WoobleTransformer(Transformer):
    number = float
    string = str

    def __init__(self):
        self.fns = {
            "def": self.define_variable,
            "*": partial(reduce, mul),
            "+": partial(reduce, add),
            "-": partial(reduce, sub),
            "/": partial(reduce, truediv)
            }
        self.vars = {}

    def define_variable(self, args):
        variable, value = args
        if not isinstance(variable, float):
            self.vars[variable] = value

    def variable(self, variable: Token):
        variable = variable.value
        return variable
    
    def contents(self, head, body):
        return [head, body]
    
    def head(self, head: Token):
        return self.fns[head.value]
    
    def body(self, *body):
        return body
    
    def expression(self, lp, contents, rp):
        fn, args = contents
        args = [self.vars.get(a, a) for a in args]
        return fn(args)
    
    def operator(self, symbol: Token):
        return symbol.value


def main():
    with open("wooble.lark", "r") as f:
        PARSER = Lark(f, start="program")
    
    TRANSFORMER = WoobleTransformer()
    
    program = """
    (def a 1)
    (def b (* 3 a))
    (def c (* a b (* 3 12) (* 4.6 0.5)))
    """

    parsed = PARSER.parse(program)
    print(parsed.pretty())
    print("=" * 80)
    transformed = TRANSFORMER.transform(parsed)
    print(f"{TRANSFORMER.vars}")


if __name__ == '__main__':
    main()