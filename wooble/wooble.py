import sys
import argparse

from collections import Iterable
from functools import partial, reduce
from operator import mul, truediv, add, sub

from lark import Lark, Transformer, v_args
from lark.lexer import Token
from toolz.itertoolz import first, rest


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", 
                        type=str, 
                        help="Path to file to be interpreted.")
    parser.add_argument("--verbose", 
                        help="Print out processing statements and order.",
                        action="store_true")
    return parser


@v_args(inline=True)
class WoobleTransformer(Transformer):
    number = float
    string = str

    def __init__(self, parser, verbose=False):
        self.verbose = verbose
        self.execution_step = 0
        self.fns = {
            "def": self.define_variable,
            "*": partial(reduce, mul),
            "+": partial(reduce, add),
            "-": partial(reduce, sub),
            "/": partial(reduce, truediv),
            "echo": self._echo
            }
        self.user_fns = {}
        self.vars = {}
        self.parser = parser
    
    def _echo(*args):
        args = map(str, first(rest(args)))
        args = map(lambda s: s.replace("\"", ""), args)
        print(" ".join(args))
    
    def parse_and_transform(self, expression):
        parsed = self.parser.parse(expression)
        transformed = self.transform(parsed)
        return transformed
    
    def function(self, fname, lp, params, rp, execution):
        self.user_fns[fname.value] = {
            "params": params.value.split(" "),
            "execution": execution.value
        }

    def print_and_inc_ex_step(self, step, tokens):
        if self.verbose:
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

            def u_fn(args):
                function_spec = self.user_fns[head.value]
                for p, a in zip(function_spec["params"], args):
                    self.define_variable((p, a))
                return self.parse_and_transform(function_spec["execution"])
                
            fn = u_fn
        return fn
    
    def body(self, *body):
        self.print_and_inc_ex_step("body", body)
        return body
    
    @staticmethod
    def _make_iterable(item):
        return item if isinstance(item, Iterable) else [item]
    
    def expression(self, lp, contents, rp):
        if contents:
            self.print_and_inc_ex_step("expression", contents)
            fn, args = contents
            args = self._make_iterable(args)
            args = [self.vars.get(a, a) for a in args]
            return fn(args)


def main(program, verbose):
    with open("wooble.lark", "r") as f:
        PARSER = Lark(f, start="program")
    
    TRANSFORMER = WoobleTransformer(PARSER, verbose=verbose)

    parsed = PARSER.parse(program)
    
    if verbose:
        print(parsed.pretty())
        print("=" * 80)
    
    transformed = TRANSFORMER.transform(parsed)
    
    if verbose:
        print(f"Defined variables: {TRANSFORMER.vars}")
        print(f"User defined functions: {TRANSFORMER.user_fns}")


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    with open(args.file, "r") as program:
        main(program.read(), args.verbose)