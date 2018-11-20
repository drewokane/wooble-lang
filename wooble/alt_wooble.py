import argparse
import ast
import astor
import sys
import typing

from ast import (Num, Str, Expr, Load, Store, Call, FunctionDef, Name, 
                 Module, arguments, arg, Assign, List, Return)
from collections import Iterable

from lark import Lark, Transformer, v_args, Tree
from lark.lexer import Token
from toolz.itertoolz import first, rest, second, drop


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

    def define_variable(self, expression) -> Assign:
        variable: str = first(expression).id
        exp: Expr = first(list(rest(expression)))
        return Assign(
            targets=[
                Name(id=variable)
            ],
            value=exp
        )

    def define_function(self, expression) -> FunctionDef:
        fname: Name = first(expression)
        args: typing.List[Name] = second(expression)
        body: Expr = list(drop(2, expression))
        return FunctionDef(
            name=fname.id,
            args=arguments(
                args=[
                    arg(arg=a.id, annotation=None) for a in args.elts
                ],
                kwonlyargs=[],
                vararg=None,
                kwarg=None,
                defaults=[],
                kw_defaults=[]
            ),
            body=[
                Return(value=first(body))
            ],
            decorator_list=[],
            returns=None
        )
    
    def function_call(self,
                      fname: Name, 
                      parameters: typing.List[typing.Any]) -> Call:
        return Call(
                func=fname,
                args=[
                    a for a in parameters
                    ],
                    keywords=[]
                    )

    def expression(self, *expression: typing.List[Expr]):
        fname: str = first(expression)
        args: List[Expr] = list(rest(expression))

        if fname.id == "defn":
            exp = self.define_function(args)
        elif fname.id == "assign":
            exp = self.define_variable(args)
        else:
            exp = self.function_call(fname, args)
        return exp

    def number(self, number: Token) -> Num:
        float_maybe = any(map(lambda s: s in number.value, [".", "e", "E"]))
        if float_maybe:
            return Num(float(number.value))
        else:
            return Num(int(number.value))

    def string(self, string: Token) -> Str:
        return Str(string.value.replace("\"", ""))

    def reference(self, reference: Token) -> Expr:
        return Name(id=reference.value, ctx=Load())
    
    def lst(self, *elements):
        return List(elts=list(elements))


def generate_ast(program):
    with open("alt_wooble.lark", "r") as f:
        PARSER = Lark(f, start="program")
    
    TRANSFORMER = WoobleTransformer()
    
    parsed = PARSER.parse(program)

    print(parsed.pretty())

    transformed = TRANSFORMER.transform(parsed)

    body = transformed.children if isinstance(transformed, Tree) else [transformed]

    return Module(body=body)


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    with open(args.file, "r") as program:
        tree = generate_ast(program.read())
    
    print(astor.dump_tree(tree))
    print(astor.to_source(tree))